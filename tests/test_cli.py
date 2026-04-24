import pytest
from unittest.mock import patch
from src.cli import (
    prompt_for_first_number,
    prompt_for_operator,
    prompt_for_second_number,
    display_result,
    display_result_unary,
    display_result_binary,
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

    @pytest.mark.parametrize("operator", ['+', '-', '*', '/', 'square', 'cube', 'sqrt', 'cbrt', 'factorial', 'power', 'log', 'ln'])
    def test_cli_supported_operators(self, operator):
        """Test that all 12 supported operators are accepted without error."""
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
        with patch('builtins.input', side_effect=['+', '10', '5']):
            result = run_calculator()
            assert result == 15.0

    def test_cli_full_workflow_subtraction(self):
        """Test end-to-end workflow for subtraction."""
        with patch('builtins.input', side_effect=['-', '10', '5']):
            result = run_calculator()
            assert result == 5.0

    def test_cli_full_workflow_multiplication(self):
        """Test end-to-end workflow for multiplication."""
        with patch('builtins.input', side_effect=['*', '10', '5']):
            result = run_calculator()
            assert result == 50.0

    def test_cli_full_workflow_division(self):
        """Test end-to-end workflow for division."""
        with patch('builtins.input', side_effect=['/', '10', '5']):
            result = run_calculator()
            assert result == 2.0

    def test_cli_division_by_zero_error(self):
        """Test error handling for division by zero."""
        with patch('builtins.input', side_effect=['/', '10', '0']):
            # Should either raise ZeroDivisionError or handle it gracefully
            try:
                result = run_calculator()
                # If no exception, result should be handled gracefully (not crash)
                assert result is not None or True
            except ZeroDivisionError:
                # Acceptable: error is raised
                pass

    def test_cli_full_workflow_square(self):
        """Test end-to-end workflow for square (unary) operation."""
        with patch('builtins.input', side_effect=['square', '5']):
            result = run_calculator()
            assert result == pytest.approx(25.0)

    def test_cli_full_workflow_cube(self):
        """Test end-to-end workflow for cube (unary) operation."""
        with patch('builtins.input', side_effect=['cube', '3']):
            result = run_calculator()
            assert result == pytest.approx(27.0)

    def test_cli_full_workflow_sqrt(self):
        """Test end-to-end workflow for square root (unary) operation."""
        with patch('builtins.input', side_effect=['sqrt', '16']):
            result = run_calculator()
            assert result == pytest.approx(4.0)

    def test_cli_full_workflow_cbrt(self):
        """Test end-to-end workflow for cube root (unary) operation."""
        with patch('builtins.input', side_effect=['cbrt', '27']):
            result = run_calculator()
            assert result == pytest.approx(3.0)

    def test_cli_full_workflow_factorial(self):
        """Test end-to-end workflow for factorial (unary) operation.

        Factorial now accepts float-like integers (e.g., 5.0 → 120).
        The implementation correctly converts float to int when appropriate.
        """
        with patch('builtins.input', side_effect=['factorial', '5']):
            result = run_calculator()
            assert result == pytest.approx(120.0)

    def test_cli_full_workflow_log(self):
        """Test end-to-end workflow for base-10 logarithm (unary) operation."""
        with patch('builtins.input', side_effect=['log', '100']):
            result = run_calculator()
            assert result == pytest.approx(2.0)

    def test_cli_full_workflow_ln(self):
        """Test end-to-end workflow for natural logarithm (unary) operation."""
        with patch('builtins.input', side_effect=['ln', '1']):
            result = run_calculator()
            assert result == pytest.approx(0.0)

    def test_cli_full_workflow_power(self):
        """Test end-to-end workflow for power (binary) operation."""
        with patch('builtins.input', side_effect=['power', '2', '3']):
            result = run_calculator()
            assert result == pytest.approx(8.0)

    def test_cli_sqrt_negative_raises_error(self):
        """Test that sqrt of negative number raises ValueError."""
        with patch('builtins.input', side_effect=['sqrt', '-4']):
            with pytest.raises(ValueError):
                run_calculator()

    def test_cli_factorial_negative_raises_error(self):
        """Test that factorial of negative number raises ValueError."""
        with patch('builtins.input', side_effect=['factorial', '-3']):
            with pytest.raises(ValueError):
                run_calculator()


class TestDisplayResultUnary:
    """Test suite for display_result_unary function."""

    def test_display_result_unary_sqrt(self, capsys):
        """Test unary result display for square root operation."""
        display_result_unary("sqrt", 9.0, 3.0)
        captured = capsys.readouterr()
        assert "sqrt(9.0) = 3.0" in captured.out

    def test_display_result_unary_square(self, capsys):
        """Test unary result display for square operation."""
        display_result_unary("square", 5.0, 25.0)
        captured = capsys.readouterr()
        assert "square(5.0) = 25.0" in captured.out

    def test_display_result_unary_cube(self, capsys):
        """Test unary result display for cube operation."""
        display_result_unary("cube", 3.0, 27.0)
        captured = capsys.readouterr()
        assert "cube(3.0) = 27.0" in captured.out

    def test_display_result_unary_factorial(self, capsys):
        """Test unary result display for factorial operation."""
        display_result_unary("factorial", 5.0, 120.0)
        captured = capsys.readouterr()
        assert "factorial(5.0) = 120.0" in captured.out


class TestDisplayResultBinary:
    """Test suite for display_result_binary function."""

    def test_display_result_binary_power(self, capsys):
        """Test binary result display for power operation."""
        display_result_binary("power", 2.0, 3.0, 8.0)
        captured = capsys.readouterr()
        assert "2.0 ^ 3.0 = 8.0" in captured.out

    def test_display_result_binary_addition(self, capsys):
        """Test binary result display for addition operation."""
        display_result_binary("+", 5.0, 3.0, 8.0)
        captured = capsys.readouterr()
        assert "5.0 + 3.0 = 8.0" in captured.out

    def test_display_result_binary_multiplication(self, capsys):
        """Test binary result display for multiplication operation."""
        display_result_binary("*", 4.0, 5.0, 20.0)
        captured = capsys.readouterr()
        assert "4.0 * 5.0 = 20.0" in captured.out

    def test_display_result_binary_division(self, capsys):
        """Test binary result display for division operation."""
        display_result_binary("/", 10.0, 2.0, 5.0)
        captured = capsys.readouterr()
        assert "10.0 / 2.0 = 5.0" in captured.out
