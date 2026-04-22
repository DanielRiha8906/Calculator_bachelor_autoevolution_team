"""Test suite for the interactive CLI module."""

import pytest
from unittest.mock import patch, MagicMock
import io

from src.core.calculator import Calculator
from src.cli import (
    get_arity,
    get_operation_menu,
    parse_float,
    get_operands,
    interactive_session,
)


class TestGetArity:
    """Test suite for get_arity() function."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance."""
        return Calculator()

    # Test unary operations (arity=1)
    @pytest.mark.parametrize("op_name", [
        "factorial",
        "square",
        "cube",
        "square_root",
        "cube_root",
        "logarithm",
        "natural_logarithm",
    ])
    def test_get_arity_unary_operations(self, calculator, op_name):
        """Unary operations should have arity of 1."""
        assert get_arity(calculator, op_name) == 1

    # Test binary operations (arity=2)
    @pytest.mark.parametrize("op_name", [
        "add",
        "subtract",
        "multiply",
        "divide",
        "power",
    ])
    def test_get_arity_binary_operations(self, calculator, op_name):
        """Binary operations should have arity of 2."""
        assert get_arity(calculator, op_name) == 2


class TestParseFloat:
    """Test suite for parse_float() function."""

    # Happy path: valid numeric strings
    @pytest.mark.parametrize("input_str,expected", [
        ("5", 5.0),
        ("3.14", 3.14),
        ("-5", -5.0),
        ("-2.5", -2.5),
        ("1e3", 1000.0),
        ("0", 0.0),
        ("0.0", 0.0),
        ("-0.0", -0.0),
        ("1.23e-4", 1.23e-4),
    ])
    def test_parse_float_valid_inputs(self, input_str, expected):
        """parse_float should correctly convert valid numeric strings."""
        result = parse_float(input_str)
        assert result == expected

    # Edge case: very large and very small numbers
    @pytest.mark.parametrize("input_str", [
        "1e100",
        "1e-100",
        "9999999999.999999",
    ])
    def test_parse_float_extreme_numbers(self, input_str):
        """parse_float should handle very large and very small numbers."""
        result = parse_float(input_str)
        assert isinstance(result, float)

    # Error cases: invalid inputs
    @pytest.mark.parametrize("invalid_input", [
        "abc",
        "",
        "1.2.3",
        "12a",
        "a12",
        "1e2e3",
    ])
    def test_parse_float_invalid_inputs_raises_value_error(self, invalid_input):
        """parse_float should raise ValueError for non-numeric inputs."""
        with pytest.raises(ValueError):
            parse_float(invalid_input)


class TestGetOperationMenu:
    """Test suite for get_operation_menu() function."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance."""
        return Calculator()

    def test_get_operation_menu_contains_all_operations(self, calculator):
        """Menu should contain all 12 public Calculator operations."""
        menu = get_operation_menu(calculator)
        expected_ops = {
            "add", "subtract", "multiply", "divide", "power",
            "factorial", "square", "cube", "square_root", "cube_root",
            "logarithm", "natural_logarithm"
        }
        assert set(menu) == expected_ops

    def test_get_operation_menu_no_dunder_names(self, calculator):
        """Menu should not contain any dunder (double underscore) names."""
        menu = get_operation_menu(calculator)
        for name in menu:
            assert not name.startswith("_"), f"Menu contains dunder name: {name}"

    def test_get_operation_menu_only_callables(self, calculator):
        """All items in menu should be callable."""
        menu = get_operation_menu(calculator)
        for name in menu:
            method = getattr(calculator, name)
            assert callable(method), f"Menu item {name} is not callable"

    def test_get_operation_menu_returns_list(self, calculator):
        """get_operation_menu should return a list."""
        menu = get_operation_menu(calculator)
        assert isinstance(menu, list)

    def test_get_operation_menu_not_empty(self, calculator):
        """Menu should not be empty."""
        menu = get_operation_menu(calculator)
        assert len(menu) > 0


class TestGetOperands:
    """Test suite for get_operands() function."""

    @patch("builtins.input")
    def test_get_operands_arity_one(self, mock_input):
        """With arity=1, should prompt once and return single float."""
        mock_input.return_value = "5.5"
        operands = get_operands(1)
        assert operands == [5.5]
        assert mock_input.call_count == 1

    @patch("builtins.input")
    def test_get_operands_arity_two(self, mock_input):
        """With arity=2, should prompt twice and return two floats."""
        mock_input.side_effect = ["3.0", "4.0"]
        operands = get_operands(2)
        assert operands == [3.0, 4.0]
        assert mock_input.call_count == 2

    @patch("builtins.input")
    def test_get_operands_arity_three(self, mock_input):
        """With arity=3, should prompt three times and return three floats."""
        mock_input.side_effect = ["1.0", "2.0", "3.0"]
        operands = get_operands(3)
        assert operands == [1.0, 2.0, 3.0]
        assert mock_input.call_count == 3

    @patch("builtins.input")
    @patch("builtins.print")
    def test_get_operands_reprompt_on_invalid_input(self, mock_print, mock_input):
        """Should reprompt when given invalid input, then accept valid input."""
        # First call invalid, second call valid
        mock_input.side_effect = ["invalid", "5.0"]
        operands = get_operands(1)
        assert operands == [5.0]
        # Should have called input twice (once invalid, once valid)
        assert mock_input.call_count == 2
        # Should have printed error message
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_get_operands_multiple_invalid_then_valid(self, mock_print, mock_input):
        """Should handle multiple invalid inputs before accepting valid one."""
        mock_input.side_effect = ["abc", "1.2.3", "", "3.14"]
        operands = get_operands(1)
        assert operands == [3.14]
        assert mock_input.call_count == 4

    @patch("builtins.input")
    def test_get_operands_negative_numbers(self, mock_input):
        """Should correctly parse negative numbers."""
        mock_input.side_effect = ["-5.5", "-2.25"]
        operands = get_operands(2)
        assert operands == [-5.5, -2.25]

    @patch("builtins.input")
    def test_get_operands_scientific_notation(self, mock_input):
        """Should correctly parse numbers in scientific notation."""
        mock_input.side_effect = ["1e3", "2.5e-2"]
        operands = get_operands(2)
        assert operands == [1000.0, 0.025]


class TestInteractiveSession:
    """Test suite for interactive_session() function."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance."""
        return Calculator()

    @patch("builtins.input")
    @patch("builtins.print")
    def test_interactive_session_quit_with_q(self, mock_print, mock_input, calculator):
        """Session should exit cleanly when user enters 'q'."""
        mock_input.return_value = "q"
        interactive_session(calculator)
        # Should print goodbye message
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        assert any("Goodbye" in str(output) for output in printed_output)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_interactive_session_quit_with_quit(self, mock_print, mock_input, calculator):
        """Session should exit cleanly when user enters 'quit'."""
        mock_input.return_value = "quit"
        interactive_session(calculator)
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        assert any("Goodbye" in str(output) for output in printed_output)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_interactive_session_quit_with_exit(self, mock_print, mock_input, calculator):
        """Session should exit cleanly when user enters 'exit'."""
        mock_input.return_value = "exit"
        interactive_session(calculator)
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        assert any("Goodbye" in str(output) for output in printed_output)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_interactive_session_quit_case_insensitive(self, mock_print, mock_input, calculator):
        """Quit commands should be case-insensitive."""
        mock_input.return_value = "QUIT"
        interactive_session(calculator)
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        assert any("Goodbye" in str(output) for output in printed_output)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_interactive_session_perform_unary_operation(self, mock_print, mock_input, calculator):
        """Session should correctly execute unary operation (square) and print result."""
        # User selects square (operation 2, assuming operations list order)
        # For safety, find the position of square in the menu
        menu = get_operation_menu(calculator)
        square_idx = menu.index("square") + 1  # 1-indexed
        mock_input.side_effect = [str(square_idx), "5", "q"]

        interactive_session(calculator)

        printed_output = [call[0][0] for call in mock_print.call_args_list]
        # Should print result of square(5) = 25
        assert any("25" in str(output) for output in printed_output)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_interactive_session_perform_binary_operation(self, mock_print, mock_input, calculator):
        """Session should correctly execute binary operation (add) and print result."""
        menu = get_operation_menu(calculator)
        add_idx = menu.index("add") + 1  # 1-indexed
        mock_input.side_effect = [str(add_idx), "3", "4", "q"]

        interactive_session(calculator)

        printed_output = [call[0][0] for call in mock_print.call_args_list]
        # Should print result of add(3, 4) = 7
        assert any("7" in str(output) for output in printed_output)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_interactive_session_invalid_menu_selection_non_integer(self, mock_print, mock_input, calculator):
        """Session should handle non-integer menu selection gracefully."""
        mock_input.side_effect = ["abc", "q"]
        interactive_session(calculator)

        printed_output = [call[0][0] for call in mock_print.call_args_list]
        # Should print error message about invalid selection
        assert any("Invalid" in str(output) and "selection" in str(output).lower() for output in printed_output)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_interactive_session_invalid_menu_selection_out_of_range_high(self, mock_print, mock_input, calculator):
        """Session should handle out-of-range menu selection (too high) gracefully."""
        mock_input.side_effect = ["999", "q"]
        interactive_session(calculator)

        printed_output = [call[0][0] for call in mock_print.call_args_list]
        # Should print error message about out of range
        assert any("out of range" in str(output).lower() for output in printed_output)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_interactive_session_invalid_menu_selection_out_of_range_low(self, mock_print, mock_input, calculator):
        """Session should handle out-of-range menu selection (too low) gracefully."""
        mock_input.side_effect = ["0", "q"]
        interactive_session(calculator)

        printed_output = [call[0][0] for call in mock_print.call_args_list]
        # Should print error message about out of range
        assert any("out of range" in str(output).lower() for output in printed_output)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_interactive_session_division_by_zero_caught(self, mock_print, mock_input, calculator):
        """Session should catch and display error when division by zero occurs."""
        menu = get_operation_menu(calculator)
        divide_idx = menu.index("divide") + 1  # 1-indexed
        mock_input.side_effect = [str(divide_idx), "10", "0", "q"]

        interactive_session(calculator)

        printed_output = [call[0][0] for call in mock_print.call_args_list]
        # Should print error message (division by zero)
        assert any("Error" in str(output) or "division" in str(output).lower() for output in printed_output)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_interactive_session_factorial_with_float_caught(self, mock_print, mock_input, calculator):
        """Session should catch TypeError when factorial receives float from CLI."""
        menu = get_operation_menu(calculator)
        factorial_idx = menu.index("factorial") + 1  # 1-indexed
        # CLI parses as float, so factorial(5.0) will raise TypeError
        mock_input.side_effect = [str(factorial_idx), "5.0", "q"]

        interactive_session(calculator)

        printed_output = [call[0][0] for call in mock_print.call_args_list]
        # Should print error message
        assert any("Error" in str(output) for output in printed_output)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_interactive_session_continues_after_error(self, mock_print, mock_input, calculator):
        """Session should continue accepting input after an operation error."""
        menu = get_operation_menu(calculator)
        divide_idx = menu.index("divide") + 1
        add_idx = menu.index("add") + 1

        # Try division by zero, then do a valid add operation, then quit
        mock_input.side_effect = [
            str(divide_idx), "10", "0",  # Division by zero error
            str(add_idx), "2", "3",       # Valid operation
            "q"
        ]

        interactive_session(calculator)

        printed_output = [call[0][0] for call in mock_print.call_args_list]
        # Should have error message from division attempt
        assert any("Error" in str(output) for output in printed_output)
        # Should also have result from addition (5.0)
        assert any("5" in str(output) for output in printed_output)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_interactive_session_shows_menu_initially(self, mock_print, mock_input, calculator):
        """Session should display the available operations menu."""
        mock_input.return_value = "q"
        interactive_session(calculator)

        printed_output = [call[0][0] for call in mock_print.call_args_list]
        # Should display available operations
        assert any("Available" in str(output) and "operations" in str(output).lower() for output in printed_output)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_interactive_session_shows_quit_instruction(self, mock_print, mock_input, calculator):
        """Session should display quit instruction in menu."""
        mock_input.return_value = "q"
        interactive_session(calculator)

        printed_output = [call[0][0] for call in mock_print.call_args_list]
        # Should mention quit options
        assert any("quit" in str(output).lower() or "exit" in str(output).lower() for output in printed_output)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_interactive_session_negative_operands(self, mock_print, mock_input, calculator):
        """Session should handle negative operands correctly."""
        menu = get_operation_menu(calculator)
        subtract_idx = menu.index("subtract") + 1
        mock_input.side_effect = [str(subtract_idx), "-5", "-3", "q"]

        interactive_session(calculator)

        printed_output = [call[0][0] for call in mock_print.call_args_list]
        # Should calculate subtract(-5, -3) = -2
        assert any("-2" in str(output) for output in printed_output)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_interactive_session_float_operands(self, mock_print, mock_input, calculator):
        """Session should handle float operands correctly."""
        menu = get_operation_menu(calculator)
        multiply_idx = menu.index("multiply") + 1
        mock_input.side_effect = [str(multiply_idx), "2.5", "4", "q"]

        interactive_session(calculator)

        printed_output = [call[0][0] for call in mock_print.call_args_list]
        # Should calculate multiply(2.5, 4) = 10.0
        assert any("10" in str(output) for output in printed_output)


class TestRetryLimitOperands:
    """Test retry limit behavior for operand validation."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance."""
        return Calculator()

    @patch("builtins.input")
    @patch("builtins.print")
    def test_operand_retry_limit_five_invalid_inputs(self, mock_print, mock_input):
        """get_operands should return None after 5 consecutive invalid inputs."""
        mock_input.side_effect = ["a", "b", "c", "d", "e"]
        result = get_operands(arity=1, mode="interactive")
        assert result is None

    @patch("builtins.input")
    @patch("builtins.print")
    def test_operand_retry_limit_prints_termination_message(self, mock_print, mock_input):
        """get_operands should print termination message after retry limit."""
        mock_input.side_effect = ["a", "b", "c", "d", "e"]
        get_operands(arity=1, mode="interactive")
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        assert any("Maximum retry attempts" in str(output) for output in printed_output)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_operand_counter_resets_on_success(self, mock_print, mock_input):
        """Operand counter should reset after successful parse."""
        # 2 failures, then success on operand 1
        # Then 2 failures on operand 2, then success
        mock_input.side_effect = ["a", "b", "5.0", "x", "y", "3.0"]
        result = get_operands(arity=2, mode="interactive")
        assert result == [5.0, 3.0]

    @patch("builtins.input")
    @patch("builtins.print")
    def test_operand_retry_limit_per_operand(self, mock_print, mock_input):
        """Each operand should have its own 5-failure limit."""
        # Operand 1: 3 failures then success
        # Operand 2: 5 failures (should return None)
        mock_input.side_effect = ["a", "b", "c", "5.0", "x", "y", "z", "w", "v"]
        result = get_operands(arity=2, mode="interactive")
        assert result is None

    @patch("builtins.input")
    @patch("builtins.print")
    def test_operand_multiple_valid_inputs(self, mock_print, mock_input):
        """Should handle arity > 1 with all valid inputs."""
        mock_input.side_effect = ["1.0", "2.0", "3.0"]
        result = get_operands(arity=3, mode="interactive")
        assert result == [1.0, 2.0, 3.0]


class TestRetryLimitOperations:
    """Test retry limit behavior for operation validation."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance."""
        return Calculator()

    @patch("builtins.input")
    @patch("builtins.print")
    def test_operation_retry_limit_five_invalid_entries(self, mock_print, mock_input, calculator):
        """interactive_session should terminate after 5 consecutive invalid operations."""
        mock_input.side_effect = ["a", "b", "c", "d", "e"]
        interactive_session(calculator)
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        assert any("Maximum retry attempts" in str(output) for output in printed_output)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_operation_retry_limit_no_goodbye_on_termination(self, mock_print, mock_input, calculator):
        """Should not print 'Goodbye!' when session terminates due to retry limit."""
        mock_input.side_effect = ["a", "b", "c", "d", "e"]
        interactive_session(calculator)
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        # When terminated by retry limit, "Goodbye!" should not appear
        # (it only appears when user explicitly enters quit/exit/q)
        assert not any("Goodbye" in str(output) for output in printed_output)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_operation_error_message_includes_available_operations(self, mock_print, mock_input, calculator):
        """Error message for invalid operation should list available operations."""
        mock_input.side_effect = ["invalid_op", "q"]
        interactive_session(calculator)
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        output_str = " ".join(str(output) for output in printed_output)
        assert "Invalid" in output_str
        # Should include at least some operations
        assert any(op in output_str for op in ["add", "subtract", "multiply"])

    @patch("builtins.input")
    @patch("builtins.print")
    def test_operation_counter_resets_on_valid_operation(self, mock_print, mock_input, calculator):
        """Operation counter should reset after successfully selecting a valid operation."""
        menu = get_operation_menu(calculator)
        add_idx = menu.index("add") + 1
        # First: 1 invalid operation (counter = 1)
        # Then: valid operation 'add' with operands 2 and 3 (counter resets to 0)
        # Then: quit
        mock_input.side_effect = [
            "invalid1",
            str(add_idx), "2", "3",  # Valid operation, counter resets
            "q"  # Quit
        ]
        interactive_session(calculator)
        # If counter reset properly, we should see "Goodbye!"
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        assert any("Goodbye" in str(output) for output in printed_output)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_operation_retry_shows_invalid_message(self, mock_print, mock_input, calculator):
        """Should show 'Invalid selection' message for invalid operation."""
        mock_input.side_effect = ["bad_op", "q"]
        interactive_session(calculator)
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        assert any("Invalid" in str(output) and "selection" in str(output).lower() for output in printed_output)


class TestCLIModeBehavior:
    """Test CLI mode behavior (no retries, immediate failure)."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance."""
        return Calculator()

    @patch("builtins.input")
    def test_get_operands_cli_mode_invalid_raises_system_exit(self, mock_input):
        """get_operands in CLI mode should raise SystemExit on invalid input."""
        mock_input.return_value = "invalid"
        with pytest.raises(SystemExit):
            get_operands(arity=1, mode="cli")

    @patch("builtins.input")
    def test_get_operands_cli_mode_no_retry(self, mock_input):
        """get_operands in CLI mode should not retry on invalid input."""
        mock_input.return_value = "invalid"
        try:
            get_operands(arity=1, mode="cli")
        except SystemExit:
            pass
        # Should only call input once
        assert mock_input.call_count == 1

    @patch("builtins.input")
    def test_get_operands_cli_mode_valid_input_succeeds(self, mock_input):
        """get_operands in CLI mode should accept valid input."""
        mock_input.side_effect = ["5.0", "3.0"]
        result = get_operands(arity=2, mode="cli")
        assert result == [5.0, 3.0]
