"""Test suite for CLI module (src/cli.py).

Tests the run_cli(argv) function which serves as a command-line interface
to the Calculator. Tests cover happy paths (valid operations), edge cases
(floats, negative numbers), error handling (domain errors, invalid input),
and argument validation.
"""

import pytest
from io import StringIO
from unittest.mock import patch
from src.ui.cli import run_cli


class TestCLIBinaryOperations:
    """Test binary operations via CLI."""

    @pytest.mark.parametrize("argv,expected_output", [
        (['add', '5', '7'], '12\n'),
        (['add', '1.5', '2.5'], '4.0\n'),
        (['add', '-5', '-3'], '-8\n'),
        (['add', '0', '0'], '0\n'),
    ])
    def test_cli_binary_add(self, argv, expected_output):
        """Test binary add operation with various inputs."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            exit_code = run_cli(argv)
            assert exit_code == 0
            assert mock_stdout.getvalue() == expected_output

    @pytest.mark.parametrize("argv,expected_output", [
        (['subtract', '10', '3'], '7\n'),
        (['subtract', '3', '10'], '-7\n'),
        (['subtract', '-5', '-3'], '-2\n'),
        (['subtract', '0', '5'], '-5\n'),
    ])
    def test_cli_binary_subtract(self, argv, expected_output):
        """Test binary subtract operation with various inputs."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            exit_code = run_cli(argv)
            assert exit_code == 0
            assert mock_stdout.getvalue() == expected_output

    @pytest.mark.parametrize("argv,expected_output", [
        (['multiply', '4', '5'], '20\n'),
        (['multiply', '2', '3'], '6\n'),
        (['multiply', '-2', '5'], '-10\n'),
        (['multiply', '0', '100'], '0\n'),
    ])
    def test_cli_binary_multiply(self, argv, expected_output):
        """Test binary multiply operation with various inputs."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            exit_code = run_cli(argv)
            assert exit_code == 0
            assert mock_stdout.getvalue() == expected_output

    @pytest.mark.parametrize("argv,expected_output", [
        (['divide', '10', '2'], '5.0\n'),
        (['divide', '9', '3'], '3.0\n'),
        (['divide', '7', '2'], '3.5\n'),
        (['divide', '-10', '2'], '-5.0\n'),
    ])
    def test_cli_binary_divide(self, argv, expected_output):
        """Test binary divide operation with various inputs."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            exit_code = run_cli(argv)
            assert exit_code == 0
            assert mock_stdout.getvalue() == expected_output

    @pytest.mark.parametrize("argv,expected_output", [
        (['power', '2', '3'], '8\n'),
        (['power', '5', '2'], '25\n'),
        (['power', '10', '0'], '1\n'),
        (['power', '2', '10'], '1024\n'),
    ])
    def test_cli_binary_power(self, argv, expected_output):
        """Test binary power operation with various inputs."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            exit_code = run_cli(argv)
            assert exit_code == 0
            assert mock_stdout.getvalue() == expected_output


class TestCLIUnaryOperations:
    """Test unary operations via CLI."""

    @pytest.mark.parametrize("argv,expected_output", [
        (['factorial', '5'], '120\n'),
        (['factorial', '0'], '1\n'),
        (['factorial', '1'], '1\n'),
        (['factorial', '10'], '3628800\n'),
    ])
    def test_cli_unary_factorial(self, argv, expected_output):
        """Test unary factorial operation with various inputs."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            exit_code = run_cli(argv)
            assert exit_code == 0
            assert mock_stdout.getvalue() == expected_output

    @pytest.mark.parametrize("argv,expected_output", [
        (['square', '4'], '16\n'),
        (['square', '0'], '0\n'),
        (['square', '-3'], '9\n'),
        (['square', '10'], '100\n'),
    ])
    def test_cli_unary_square(self, argv, expected_output):
        """Test unary square operation with various inputs."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            exit_code = run_cli(argv)
            assert exit_code == 0
            assert mock_stdout.getvalue() == expected_output

    @pytest.mark.parametrize("argv,expected_output", [
        (['cube', '3'], '27\n'),
        (['cube', '0'], '0\n'),
        (['cube', '-2'], '-8\n'),
        (['cube', '5'], '125\n'),
    ])
    def test_cli_unary_cube(self, argv, expected_output):
        """Test unary cube operation with various inputs."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            exit_code = run_cli(argv)
            assert exit_code == 0
            assert mock_stdout.getvalue() == expected_output

    def test_cli_unary_sqrt_valid(self):
        """Test unary sqrt operation with valid input."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            exit_code = run_cli(['sqrt', '9'])
            assert exit_code == 0
            output = mock_stdout.getvalue().strip()
            assert float(output) == pytest.approx(3.0, rel=1e-5)

    def test_cli_unary_cbrt_valid(self):
        """Test unary cbrt operation with valid input."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            exit_code = run_cli(['cbrt', '8'])
            assert exit_code == 0
            output = mock_stdout.getvalue().strip()
            assert float(output) == pytest.approx(2.0, rel=1e-5)

    def test_cli_unary_ln_valid(self):
        """Test unary ln operation with valid input."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            exit_code = run_cli(['ln', '2.718281828'])
            assert exit_code == 0
            output = mock_stdout.getvalue().strip()
            assert float(output) == pytest.approx(1.0, rel=1e-3)

    def test_cli_unary_log10_valid(self):
        """Test unary log10 operation with valid input."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            exit_code = run_cli(['log10', '100'])
            assert exit_code == 0
            output = mock_stdout.getvalue().strip()
            assert float(output) == pytest.approx(2.0, rel=1e-5)


class TestCLIFloatAndNegativeOperands:
    """Test CLI with float and negative operands."""

    def test_cli_float_operands_binary(self):
        """Test binary operation with float operands."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            exit_code = run_cli(['add', '1.5', '2.5'])
            assert exit_code == 0
            output = mock_stdout.getvalue().strip()
            assert float(output) == pytest.approx(4.0, rel=1e-5)

    def test_cli_negative_operands(self):
        """Test binary operation with negative operands."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            exit_code = run_cli(['add', '-5', '-3'])
            assert exit_code == 0
            output = mock_stdout.getvalue().strip()
            assert float(output) == pytest.approx(-8, rel=1e-5)

    def test_cli_large_number_computation(self):
        """Test computation with large numbers."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            exit_code = run_cli(['multiply', '1000000', '1000000'])
            assert exit_code == 0
            output = mock_stdout.getvalue().strip()
            assert float(output) == pytest.approx(1000000000000, rel=1e-5)


class TestCLIDomainErrors:
    """Test CLI error handling for domain errors."""

    def test_cli_division_by_zero_error(self):
        """Test division by zero error."""
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            exit_code = run_cli(['divide', '5', '0'])
            assert exit_code == 1
            error_output = mock_stderr.getvalue().lower()
            assert 'division by zero' in error_output or 'zero' in error_output

    def test_cli_sqrt_negative_error(self):
        """Test sqrt of negative number error."""
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            exit_code = run_cli(['sqrt', '-4'])
            assert exit_code == 1
            error_output = mock_stderr.getvalue()
            assert len(error_output) > 0  # Any error message is acceptable

    def test_cli_factorial_negative_error(self):
        """Test factorial of negative number error."""
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            exit_code = run_cli(['factorial', '-5'])
            assert exit_code == 1
            error_output = mock_stderr.getvalue()
            assert len(error_output) > 0  # Any error message is acceptable

    def test_cli_log10_negative_error(self):
        """Test log10 of negative number error."""
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            exit_code = run_cli(['log10', '-1'])
            assert exit_code == 1
            error_output = mock_stderr.getvalue()
            assert len(error_output) > 0  # Any error message is acceptable

    def test_cli_ln_zero_error(self):
        """Test ln of zero error."""
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            exit_code = run_cli(['ln', '0'])
            assert exit_code == 1
            error_output = mock_stderr.getvalue()
            assert len(error_output) > 0  # Any error message is acceptable


class TestCLIArgumentValidation:
    """Test CLI argument validation errors."""

    def test_cli_missing_operation_argument(self):
        """Test missing operation argument."""
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            exit_code = run_cli([])
            assert exit_code == 1
            error_output = mock_stderr.getvalue()
            assert len(error_output) > 0  # Usage hint or error message

    def test_cli_missing_operands_unary(self):
        """Test missing operand for unary operation."""
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            exit_code = run_cli(['factorial'])
            assert exit_code == 1
            error_output = mock_stderr.getvalue()
            assert len(error_output) > 0  # Any error message is acceptable

    def test_cli_missing_operands_binary(self):
        """Test missing operand for binary operation."""
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            exit_code = run_cli(['add', '5'])
            assert exit_code == 1
            error_output = mock_stderr.getvalue()
            assert len(error_output) > 0  # Any error message is acceptable

    def test_cli_too_many_operands_unary(self):
        """Test too many operands for unary operation."""
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            exit_code = run_cli(['factorial', '5', '6'])
            assert exit_code == 1
            error_output = mock_stderr.getvalue()
            assert len(error_output) > 0  # Any error message is acceptable

    def test_cli_too_many_operands_binary(self):
        """Test too many operands for binary operation."""
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            exit_code = run_cli(['add', '5', '7', '9'])
            assert exit_code == 1
            error_output = mock_stderr.getvalue()
            assert len(error_output) > 0  # Any error message is acceptable

    def test_cli_unknown_operation(self):
        """Test unknown operation."""
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            exit_code = run_cli(['unknown_op', '5'])
            assert exit_code == 1
            error_output = mock_stderr.getvalue()
            assert len(error_output) > 0  # Any error message is acceptable


class TestCLIOperandFormatErrors:
    """Test CLI operand format errors."""

    def test_cli_non_numeric_operand(self):
        """Test non-numeric operand."""
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            exit_code = run_cli(['add', 'abc', '5'])
            assert exit_code == 1
            error_output = mock_stderr.getvalue()
            assert len(error_output) > 0  # Any error message is acceptable

    def test_cli_non_numeric_second_operand(self):
        """Test non-numeric second operand."""
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            exit_code = run_cli(['add', '5', 'xyz'])
            assert exit_code == 1
            error_output = mock_stderr.getvalue()
            assert len(error_output) > 0  # Any error message is acceptable

    def test_cli_non_numeric_unary_operand(self):
        """Test non-numeric operand for unary operation."""
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            exit_code = run_cli(['factorial', 'abc'])
            assert exit_code == 1
            error_output = mock_stderr.getvalue()
            assert len(error_output) > 0  # Any error message is acceptable
