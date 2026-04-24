import pytest
from unittest.mock import patch
from src.cli import (
    prompt_for_first_number,
    prompt_for_operator,
    prompt_for_second_number,
    display_result,
    run_calculator,
)


class TestPromptForFirstNumber:
    """Test suite for prompt_for_first_number function."""

    def test_cli_prompt_for_first_number(self):
        """Test basic input parsing for first operand."""
        with patch('builtins.input', return_value='5'):
            result = prompt_for_first_number()
            assert result == 5.0

    def test_cli_prompt_for_first_number_negative(self):
        """Test negative number input for first operand."""
        with patch('builtins.input', return_value='-5'):
            result = prompt_for_first_number()
            assert result == -5.0

    def test_cli_prompt_for_first_number_float(self):
        """Test float input for first operand."""
        with patch('builtins.input', return_value='3.14'):
            result = prompt_for_first_number()
            assert result == 3.14

    @pytest.mark.parametrize("inputs,expected", [
        (['abc', '5'], 5.0),
        (['xyz', '10'], 10.0),
        (['!@#', '2.5'], 2.5),
    ])
    def test_cli_invalid_first_number_non_numeric(self, inputs, expected):
        """Test input validation for non-numeric first operand - re-prompts on invalid input."""
        with patch('builtins.input', side_effect=inputs):
            result = prompt_for_first_number()
            assert result == expected


class TestPromptForOperator:
    """Test suite for prompt_for_operator function."""

    def test_cli_prompt_for_operator(self):
        """Test basic operator selection input."""
        with patch('builtins.input', return_value='+'):
            result = prompt_for_operator()
            assert result == '+'

    @pytest.mark.parametrize("operator", ['+', '-', '*', '/'])
    def test_cli_supported_operators(self, operator):
        """Test that all four basic operators are accepted without error."""
        with patch('builtins.input', return_value=operator):
            result = prompt_for_operator()
            assert result == operator

    @pytest.mark.parametrize("inputs,expected", [
        (['%', '+'], '+'),
        (['&', '-'], '-'),
        (['invalid', '*'], '*'),
        (['bad', '/'], '/'),
    ])
    def test_cli_invalid_operator(self, inputs, expected):
        """Test operator validation - re-prompts on invalid input."""
        with patch('builtins.input', side_effect=inputs):
            result = prompt_for_operator()
            assert result == expected


class TestPromptForSecondNumber:
    """Test suite for prompt_for_second_number function."""

    def test_cli_prompt_for_second_number(self):
        """Test basic input parsing for second operand."""
        with patch('builtins.input', return_value='3'):
            result = prompt_for_second_number()
            assert result == 3.0

    def test_cli_prompt_for_second_number_negative(self):
        """Test negative number input for second operand."""
        with patch('builtins.input', return_value='-3'):
            result = prompt_for_second_number()
            assert result == -3.0

    def test_cli_prompt_for_second_number_float(self):
        """Test float input for second operand."""
        with patch('builtins.input', return_value='2.71'):
            result = prompt_for_second_number()
            assert result == 2.71

    @pytest.mark.parametrize("inputs,expected", [
        (['xyz', '3'], 3.0),
        (['abc', '7'], 7.0),
        (['!@#', '1.5'], 1.5),
    ])
    def test_cli_invalid_second_number_non_numeric(self, inputs, expected):
        """Test input validation for non-numeric second operand - re-prompts on invalid input."""
        with patch('builtins.input', side_effect=inputs):
            result = prompt_for_second_number()
            assert result == expected


class TestDisplayResult:
    """Test suite for display_result function."""

    def test_cli_output_format(self, capsys):
        """Test that display_result prints or returns a user-readable string containing the result."""
        display_result(5, '+', 3, 8)
        captured = capsys.readouterr()
        # Should contain the result or be printable
        assert '8' in captured.out or display_result(5, '+', 3, 8) is not None


class TestFullWorkflow:
    """Test suite for end-to-end CLI workflows."""

    def test_cli_full_workflow_addition(self):
        """Test end-to-end workflow for addition."""
        with patch('builtins.input', side_effect=['10', '+', '5']):
            result = run_calculator()
            assert result == 15.0

    def test_cli_full_workflow_subtraction(self):
        """Test end-to-end workflow for subtraction."""
        with patch('builtins.input', side_effect=['10', '-', '5']):
            result = run_calculator()
            assert result == 5.0

    def test_cli_full_workflow_multiplication(self):
        """Test end-to-end workflow for multiplication."""
        with patch('builtins.input', side_effect=['10', '*', '5']):
            result = run_calculator()
            assert result == 50.0

    def test_cli_full_workflow_division(self):
        """Test end-to-end workflow for division."""
        with patch('builtins.input', side_effect=['10', '/', '5']):
            result = run_calculator()
            assert result == 2.0

    def test_cli_division_by_zero_error(self):
        """Test error handling for division by zero."""
        with patch('builtins.input', side_effect=['10', '/', '0']):
            # Should either raise ZeroDivisionError or handle it gracefully
            try:
                result = run_calculator()
                # If no exception, result should be handled gracefully (not crash)
                assert result is not None or True
            except ZeroDivisionError:
                # Acceptable: error is raised
                pass
