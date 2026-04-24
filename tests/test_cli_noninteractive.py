"""Non-interactive CLI mode tests for the calculator.

Tests the command-line interface for non-interactive operation mode where
arguments are passed directly (e.g., `python -m calculator add 10 5`)
rather than via interactive prompts.
"""

import pytest
import subprocess
from src.cli import main_cli_noninteractive


class TestBinaryOperations:
    """Test suite for binary CLI operations."""

    @pytest.mark.parametrize("operation,operands,expected", [
        ("add", ["10", "5"], "15"),
        ("subtract", ["10", "5"], "5"),
        ("multiply", ["4", "6"], "24"),
        ("divide", ["20", "4"], "5.0"),
        ("power", ["2", "8"], "256"),
    ])
    def test_cli_binary_operations(self, operation, operands, expected, capsys):
        """Test binary operations (add, subtract, multiply, divide, power) via CLI."""
        args = [operation] + operands
        exit_code = main_cli_noninteractive(args)

        captured = capsys.readouterr()
        assert expected in captured.out
        assert exit_code == 0


class TestUnaryOperations:
    """Test suite for unary CLI operations."""

    @pytest.mark.parametrize("operation,operand,expected", [
        ("square", "7", "49"),
        ("cube", "3", "27"),
        ("sqrt", "16", "4.0"),
        ("cbrt", "8", "2.0"),
        ("factorial", "5", "120"),
        ("log", "100", "2.0"),
        ("ln", "2.718281828", "1.0"),
    ])
    def test_cli_unary_operations(self, operation, operand, expected, capsys):
        """Test unary operations (square, cube, sqrt, cbrt, factorial, log, ln) via CLI."""
        args = [operation, operand]
        exit_code = main_cli_noninteractive(args)

        captured = capsys.readouterr()
        # Use approx comparison for floating-point operations
        if "." in expected:
            # For log and ln, allow some tolerance
            try:
                actual = float(captured.out.strip().split()[-1])
                assert actual == pytest.approx(float(expected), rel=1e-2)
            except (ValueError, IndexError):
                pytest.fail(f"Could not parse output: {captured.out}")
        else:
            assert expected in captured.out
        assert exit_code == 0


class TestFloatOperands:
    """Test suite for float and negative operands."""

    def test_cli_float_operands_binary(self, capsys):
        """Test binary operation with float operands."""
        args = ["add", "3.5", "2.5"]
        exit_code = main_cli_noninteractive(args)

        captured = capsys.readouterr()
        assert "6.0" in captured.out
        assert exit_code == 0

    def test_cli_float_operands_unary(self, capsys):
        """Test unary operation with float operand."""
        args = ["square", "2.5"]
        exit_code = main_cli_noninteractive(args)

        captured = capsys.readouterr()
        assert "6.25" in captured.out
        assert exit_code == 0

    def test_cli_negative_operands_binary(self, capsys):
        """Test binary operation with negative operands."""
        args = ["multiply", "-3", "4"]
        exit_code = main_cli_noninteractive(args)

        captured = capsys.readouterr()
        assert "-12" in captured.out
        assert exit_code == 0

    def test_cli_negative_operands_unary(self, capsys):
        """Test unary operation with negative operand."""
        args = ["cube", "-2"]
        exit_code = main_cli_noninteractive(args)

        captured = capsys.readouterr()
        assert "-8" in captured.out
        assert exit_code == 0


class TestDivisionByZero:
    """Test suite for division by zero error handling."""

    def test_cli_division_by_zero(self, capsys):
        """Test that division by zero produces an error."""
        args = ["divide", "10", "0"]
        exit_code = main_cli_noninteractive(args)

        captured = capsys.readouterr()
        # Error should be in stderr or output should indicate error
        assert captured.err or "Error" in captured.out or "error" in captured.out.lower()
        assert exit_code != 0


class TestDomainErrors:
    """Test suite for domain errors (math domain errors)."""

    def test_cli_sqrt_negative(self, capsys):
        """Test that sqrt of negative number produces an error."""
        args = ["sqrt", "-4"]
        exit_code = main_cli_noninteractive(args)

        captured = capsys.readouterr()
        assert captured.err or "Error" in captured.out or "error" in captured.out.lower()
        assert exit_code != 0

    def test_cli_log_zero(self, capsys):
        """Test that log(0) produces an error."""
        args = ["log", "0"]
        exit_code = main_cli_noninteractive(args)

        captured = capsys.readouterr()
        assert captured.err or "Error" in captured.out or "error" in captured.out.lower()
        assert exit_code != 0

    def test_cli_log_negative(self, capsys):
        """Test that log of negative number produces an error."""
        args = ["log", "-5"]
        exit_code = main_cli_noninteractive(args)

        captured = capsys.readouterr()
        assert captured.err or "Error" in captured.out or "error" in captured.out.lower()
        assert exit_code != 0

    def test_cli_ln_zero(self, capsys):
        """Test that ln(0) produces an error."""
        args = ["ln", "0"]
        exit_code = main_cli_noninteractive(args)

        captured = capsys.readouterr()
        assert captured.err or "Error" in captured.out or "error" in captured.out.lower()
        assert exit_code != 0

    def test_cli_factorial_negative(self, capsys):
        """Test that factorial of negative number produces an error."""
        args = ["factorial", "-1"]
        exit_code = main_cli_noninteractive(args)

        captured = capsys.readouterr()
        assert captured.err or "Error" in captured.out or "error" in captured.out.lower()
        assert exit_code != 0

    def test_cli_factorial_float_non_integer(self, capsys):
        """Test that factorial of non-integer float produces an error."""
        args = ["factorial", "5.5"]
        exit_code = main_cli_noninteractive(args)

        captured = capsys.readouterr()
        assert captured.err or "Error" in captured.out or "error" in captured.out.lower()
        assert exit_code != 0


class TestInvalidInputHandling:
    """Test suite for invalid input error handling."""

    def test_cli_invalid_operation_name(self, capsys):
        """Test that invalid operation name produces an error."""
        args = ["invalid_op", "5", "3"]
        exit_code = main_cli_noninteractive(args)

        captured = capsys.readouterr()
        assert captured.err or "Error" in captured.out or "error" in captured.out.lower()
        assert exit_code != 0

    def test_cli_missing_operand_unary(self, capsys):
        """Test that missing operand for unary operation produces an error."""
        args = ["square"]
        exit_code = main_cli_noninteractive(args)

        captured = capsys.readouterr()
        assert captured.err or "Error" in captured.out or "error" in captured.out.lower()
        assert exit_code != 0

    def test_cli_missing_operand_binary(self, capsys):
        """Test that missing second operand for binary operation produces an error."""
        args = ["add", "5"]
        exit_code = main_cli_noninteractive(args)

        captured = capsys.readouterr()
        assert captured.err or "Error" in captured.out or "error" in captured.out.lower()
        assert exit_code != 0

    def test_cli_non_numeric_operand_unary(self, capsys):
        """Test that non-numeric operand for unary operation produces an error."""
        args = ["square", "abc"]
        exit_code = main_cli_noninteractive(args)

        captured = capsys.readouterr()
        assert captured.err or "Error" in captured.out or "error" in captured.out.lower()
        assert exit_code != 0

    def test_cli_non_numeric_operand_binary(self, capsys):
        """Test that non-numeric operand for binary operation produces an error."""
        args = ["add", "5", "xyz"]
        exit_code = main_cli_noninteractive(args)

        captured = capsys.readouterr()
        assert captured.err or "Error" in captured.out or "error" in captured.out.lower()
        assert exit_code != 0


class TestSubprocessIntegration:
    """Test suite for subprocess-based integration tests."""

    def test_cli_subprocess_valid_addition(self):
        """Test non-interactive CLI via subprocess for valid addition."""
        result = subprocess.run(
            ["python", "-m", "calculator", "add", "2", "3"],
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            capture_output=True,
            text=True
        )
        # Should produce '5' in output and exit with 0
        assert "5" in result.stdout, f"Expected '5' in stdout, got: {result.stdout}, stderr: {result.stderr}"
        assert result.returncode == 0, f"Expected returncode 0, got {result.returncode}"

    def test_cli_subprocess_division_by_zero(self):
        """Test non-interactive CLI via subprocess for division by zero."""
        result = subprocess.run(
            ["python", "-m", "calculator", "divide", "10", "0"],
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            capture_output=True,
            text=True
        )
        # Should produce error message (containing "division by zero" or similar) and non-zero exit code
        # Must not be a module-not-found error
        assert "No module named" not in result.stderr, f"Module not found, implementation missing: {result.stderr}"
        has_error = result.stderr or ("error" in result.stdout.lower() or "Error" in result.stdout)
        assert has_error, f"Expected error message in stdout or stderr, got stdout: {result.stdout}, stderr: {result.stderr}"
        assert result.returncode != 0, f"Expected non-zero returncode, got {result.returncode}"

    def test_cli_subprocess_sqrt_negative(self):
        """Test non-interactive CLI via subprocess for sqrt of negative."""
        result = subprocess.run(
            ["python", "-m", "calculator", "sqrt", "-1"],
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            capture_output=True,
            text=True
        )
        # Should produce error message (for negative sqrt) and non-zero exit code
        # Must not be a module-not-found error
        assert "No module named" not in result.stderr, f"Module not found, implementation missing: {result.stderr}"
        has_error = result.stderr or ("error" in result.stdout.lower() or "Error" in result.stdout)
        assert has_error, f"Expected error message in stdout or stderr, got stdout: {result.stdout}, stderr: {result.stderr}"
        assert result.returncode != 0, f"Expected non-zero returncode, got {result.returncode}"


class TestHelpAndUsage:
    """Test suite for help and usage information."""

    @pytest.mark.parametrize("flag", ["--help", "-h"])
    def test_cli_help_flag(self, flag, capsys):
        """Test that help flag displays usage information."""
        args = [flag]
        try:
            exit_code = main_cli_noninteractive(args)
            # help should exit with code 0
            assert exit_code == 0 or exit_code is None
        except SystemExit as e:
            # argparse default help behavior raises SystemExit(0)
            assert e.code == 0

        captured = capsys.readouterr()
        # Should contain usage or help information
        assert captured.out or captured.err

    def test_cli_no_arguments(self, capsys):
        """Test that running with no arguments produces an error or usage message."""
        args = []
        exit_code = main_cli_noninteractive(args)

        captured = capsys.readouterr()
        # Should produce error or usage info
        assert exit_code != 0 or captured.out or captured.err
