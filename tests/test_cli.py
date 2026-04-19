"""Comprehensive pytest tests for the CLI module.

This module tests three main functions from src.cli:
- parse_arguments(): CLI argument parsing
- convert_operand(): string-to-number conversion
- execute_cli(): operation dispatch and execution

Tests cover normal cases, edge cases, and error handling.
"""

import subprocess
import sys
from pathlib import Path

import pytest

from src.calculator import Calculator
from src.cli import convert_operand, execute_cli, parse_arguments
from src.input_handler import get_operation_registry


# ==================== convert_operand() Tests ====================

class TestConvertOperand:
    """Tests for the convert_operand() function."""

    def test_convert_operand_integer(self):
        """Test parsing a simple integer string: "5" -> 5 (int)."""
        result = convert_operand("5")
        assert result == 5
        assert isinstance(result, int)

    def test_convert_operand_float(self):
        """Test parsing a decimal string: "3.14" -> 3.14 (float)."""
        result = convert_operand("3.14")
        assert result == 3.14
        assert isinstance(result, float)

    def test_convert_operand_negative_integer(self):
        """Test parsing a negative integer: "-10" -> -10 (int)."""
        result = convert_operand("-10")
        assert result == -10
        assert isinstance(result, int)

    def test_convert_operand_negative_float(self):
        """Test parsing a negative float: "-2.5" -> -2.5 (float)."""
        result = convert_operand("-2.5")
        assert result == -2.5
        assert isinstance(result, float)

    def test_convert_operand_zero(self):
        """Test parsing zero: "0" -> 0 (int)."""
        result = convert_operand("0")
        assert result == 0
        assert isinstance(result, int)

    def test_convert_operand_zero_float(self):
        """Test parsing zero as float: "0.0" -> 0 (int, since 0.0 == int(0.0))."""
        result = convert_operand("0.0")
        assert result == 0
        assert isinstance(result, int)

    def test_convert_operand_whole_float(self):
        """Test parsing a whole number as float: "5.0" -> 5 (int)."""
        result = convert_operand("5.0")
        assert result == 5
        assert isinstance(result, int)

    def test_convert_operand_fractional_float(self):
        """Test parsing a non-whole float: "5.5" -> 5.5 (float)."""
        result = convert_operand("5.5")
        assert result == 5.5
        assert isinstance(result, float)

    def test_convert_operand_large_integer(self):
        """Test parsing a large integer: "999999999" -> 999999999 (int)."""
        result = convert_operand("999999999")
        assert result == 999999999
        assert isinstance(result, int)

    def test_convert_operand_very_small_float(self):
        """Test parsing a very small float: "0.0001" -> 0.0001 (float)."""
        result = convert_operand("0.0001")
        assert result == 0.0001
        assert isinstance(result, float)

    def test_convert_operand_scientific_notation(self):
        """Test parsing scientific notation: "1e3" -> 1000.0 (float as whole)."""
        result = convert_operand("1e3")
        assert result == 1000
        assert isinstance(result, int)

    def test_convert_operand_scientific_notation_non_whole(self):
        """Test parsing scientific notation: "1.5e2" -> 150.0 (float as whole)."""
        result = convert_operand("1.5e2")
        assert result == 150
        assert isinstance(result, int)

    def test_convert_operand_leading_zeros(self):
        """Test parsing with leading zeros: "007" -> 7 (int)."""
        result = convert_operand("007")
        assert result == 7
        assert isinstance(result, int)

    def test_convert_operand_trailing_zeros(self):
        """Test parsing with trailing zeros: "5.000" -> 5 (int)."""
        result = convert_operand("5.000")
        assert result == 5
        assert isinstance(result, int)

    def test_convert_operand_invalid_string_raises_error(self):
        """Test that parsing non-numeric string raises ValueError: "abc"."""
        with pytest.raises(ValueError, match="operand 'abc' is not a valid number"):
            convert_operand("abc")

    def test_convert_operand_empty_string_raises_error(self):
        """Test that parsing empty string raises ValueError."""
        with pytest.raises(ValueError):
            convert_operand("")

    def test_convert_operand_whitespace_only_raises_error(self):
        """Test that parsing whitespace-only string raises ValueError."""
        with pytest.raises(ValueError):
            convert_operand("   ")

    def test_convert_operand_mixed_alpha_numeric_raises_error(self):
        """Test that parsing mixed alphanumeric raises ValueError: "12abc"."""
        with pytest.raises(ValueError):
            convert_operand("12abc")

    def test_convert_operand_special_characters_raises_error(self):
        """Test that parsing special characters raises ValueError: "3!5"."""
        with pytest.raises(ValueError):
            convert_operand("3!5")

    def test_convert_operand_inf_raises_error(self):
        """Test parsing infinity raises OverflowError (caught as ValueError in practice)."""
        # Note: convert_operand doesn't handle infinity gracefully due to int() conversion
        # This is an edge case that the implementation doesn't support
        with pytest.raises((OverflowError, ValueError)):
            convert_operand("inf")

    def test_convert_operand_negative_inf_raises_error(self):
        """Test parsing negative infinity raises OverflowError."""
        with pytest.raises((OverflowError, ValueError)):
            convert_operand("-inf")

    def test_convert_operand_nan_raises_error(self):
        """Test parsing NaN raises ValueError."""
        with pytest.raises((ValueError, OverflowError)):
            convert_operand("nan")


# ==================== parse_arguments() Tests ====================

class TestParseArguments:
    """Tests for the parse_arguments() function."""

    def test_parse_arguments_binary_op(self):
        """Test parsing binary operation: ["add", "5", "3"]."""
        operation_name, operands = parse_arguments(["add", "5", "3"])
        assert operation_name == "add"
        assert operands == ["5", "3"]

    def test_parse_arguments_unary_op(self):
        """Test parsing unary operation: ["factorial", "5"]."""
        operation_name, operands = parse_arguments(["factorial", "5"])
        assert operation_name == "factorial"
        assert operands == ["5"]

    def test_parse_arguments_single_arg_only_operation_name(self):
        """Test parsing with just operation name: ["add"]."""
        operation_name, operands = parse_arguments(["add"])
        assert operation_name == "add"
        assert operands == []

    def test_parse_arguments_multiple_operands(self):
        """Test parsing with three operands (though CLI doesn't support ternary)."""
        operation_name, operands = parse_arguments(["op", "1", "2", "3"])
        assert operation_name == "op"
        assert operands == ["1", "2", "3"]

    def test_parse_arguments_operation_name_with_underscore(self):
        """Test parsing operation name with underscore: "square_root"."""
        operation_name, operands = parse_arguments(["square_root", "9"])
        assert operation_name == "square_root"
        assert operands == ["9"]

    def test_parse_arguments_negative_operands(self):
        """Test parsing with negative operand strings."""
        operation_name, operands = parse_arguments(["subtract", "-5", "-3"])
        assert operation_name == "subtract"
        assert operands == ["-5", "-3"]

    def test_parse_arguments_float_operands(self):
        """Test parsing with float operand strings."""
        operation_name, operands = parse_arguments(["divide", "10.5", "2.5"])
        assert operation_name == "divide"
        assert operands == ["10.5", "2.5"]

    def test_parse_arguments_zero_operand(self):
        """Test parsing with zero as operand."""
        operation_name, operands = parse_arguments(["add", "0", "5"])
        assert operation_name == "add"
        assert operands == ["0", "5"]

    def test_parse_arguments_whitespace_in_operands(self):
        """Test that whitespace is preserved in operand strings (no stripping in parse_arguments)."""
        operation_name, operands = parse_arguments(["add", " 5 ", " 3 "])
        assert operation_name == "add"
        assert operands == [" 5 ", " 3 "]


# ==================== execute_cli() Success Tests ====================

class TestExecuteCliSuccess:
    """Tests for execute_cli() success cases."""

    @pytest.fixture
    def calc_and_registry(self):
        """Fixture to create a Calculator instance and registry."""
        calculator = Calculator()
        registry = get_operation_registry(calculator)
        return calculator, registry

    def test_execute_cli_add(self, capsys, calc_and_registry):
        """Test executing add operation: 5 + 7 = 12."""
        calc, registry = calc_and_registry
        result = execute_cli("add", ["5", "7"], registry, calc)
        captured = capsys.readouterr()
        assert result == 0
        assert "12" in captured.out

    def test_execute_cli_subtract(self, capsys, calc_and_registry):
        """Test executing subtract operation: 10 - 3 = 7."""
        calc, registry = calc_and_registry
        result = execute_cli("subtract", ["10", "3"], registry, calc)
        captured = capsys.readouterr()
        assert result == 0
        assert "7" in captured.out

    def test_execute_cli_multiply(self, capsys, calc_and_registry):
        """Test executing multiply operation: 4 * 5 = 20."""
        calc, registry = calc_and_registry
        result = execute_cli("multiply", ["4", "5"], registry, calc)
        captured = capsys.readouterr()
        assert result == 0
        assert "20" in captured.out

    def test_execute_cli_divide(self, capsys, calc_and_registry):
        """Test executing divide operation: 10 / 2 = 5.0."""
        calc, registry = calc_and_registry
        result = execute_cli("divide", ["10", "2"], registry, calc)
        captured = capsys.readouterr()
        assert result == 0
        assert "5" in captured.out

    def test_execute_cli_factorial(self, capsys, calc_and_registry):
        """Test executing factorial operation: factorial(5) = 120."""
        calc, registry = calc_and_registry
        result = execute_cli("factorial", ["5"], registry, calc)
        captured = capsys.readouterr()
        assert result == 0
        assert "120" in captured.out

    def test_execute_cli_square(self, capsys, calc_and_registry):
        """Test executing square operation: square(4) = 16."""
        calc, registry = calc_and_registry
        result = execute_cli("square", ["4"], registry, calc)
        captured = capsys.readouterr()
        assert result == 0
        assert "16" in captured.out

    def test_execute_cli_cube(self, capsys, calc_and_registry):
        """Test executing cube operation: cube(3) = 27."""
        calc, registry = calc_and_registry
        result = execute_cli("cube", ["3"], registry, calc)
        captured = capsys.readouterr()
        assert result == 0
        assert "27" in captured.out

    def test_execute_cli_square_root(self, capsys, calc_and_registry):
        """Test executing square_root operation: square_root(9) = 3.0."""
        calc, registry = calc_and_registry
        result = execute_cli("square_root", ["9"], registry, calc)
        captured = capsys.readouterr()
        assert result == 0
        assert "3" in captured.out

    def test_execute_cli_power(self, capsys, calc_and_registry):
        """Test executing power operation: power(2, 10) = 1024."""
        calc, registry = calc_and_registry
        result = execute_cli("power", ["2", "10"], registry, calc)
        captured = capsys.readouterr()
        assert result == 0
        assert "1024" in captured.out

    def test_execute_cli_log(self, capsys, calc_and_registry):
        """Test executing log operation: log(100) = 2.0."""
        calc, registry = calc_and_registry
        result = execute_cli("log", ["100"], registry, calc)
        captured = capsys.readouterr()
        assert result == 0
        assert "2" in captured.out

    def test_execute_cli_ln(self, capsys, calc_and_registry):
        """Test executing ln operation: ln(e) ≈ 1.0."""
        import math
        calc, registry = calc_and_registry
        result = execute_cli("ln", [str(math.e)], registry, calc)
        captured = capsys.readouterr()
        assert result == 0
        # Result should be close to 1.0
        assert "1" in captured.out

    def test_execute_cli_cube_root(self, capsys, calc_and_registry):
        """Test executing cube_root operation: cube_root(27) = 3.0."""
        calc, registry = calc_and_registry
        result = execute_cli("cube_root", ["27"], registry, calc)
        captured = capsys.readouterr()
        assert result == 0
        assert "3" in captured.out

    def test_execute_cli_add_negative_numbers(self, capsys, calc_and_registry):
        """Test add with negative operands: -5 + 3 = -2."""
        calc, registry = calc_and_registry
        result = execute_cli("add", ["-5", "3"], registry, calc)
        captured = capsys.readouterr()
        assert result == 0
        assert "-2" in captured.out

    def test_execute_cli_add_floats(self, capsys, calc_and_registry):
        """Test add with float operands: 2.5 + 1.5 = 4.0."""
        calc, registry = calc_and_registry
        result = execute_cli("add", ["2.5", "1.5"], registry, calc)
        captured = capsys.readouterr()
        assert result == 0
        assert "4" in captured.out

    def test_execute_cli_factorial_zero(self, capsys, calc_and_registry):
        """Test factorial(0) = 1."""
        calc, registry = calc_and_registry
        result = execute_cli("factorial", ["0"], registry, calc)
        captured = capsys.readouterr()
        assert result == 0
        assert "1" in captured.out

    def test_execute_cli_factorial_one(self, capsys, calc_and_registry):
        """Test factorial(1) = 1."""
        calc, registry = calc_and_registry
        result = execute_cli("factorial", ["1"], registry, calc)
        captured = capsys.readouterr()
        assert result == 0
        assert "1" in captured.out


# ==================== execute_cli() Error Tests ====================

class TestExecuteCliErrors:
    """Tests for execute_cli() error handling."""

    @pytest.fixture
    def calc_and_registry(self):
        """Fixture to create a Calculator instance and registry."""
        calculator = Calculator()
        registry = get_operation_registry(calculator)
        return calculator, registry

    def test_execute_cli_unknown_operation(self, capsys, calc_and_registry):
        """Test unknown operation returns 1 with error message."""
        calc, registry = calc_and_registry
        result = execute_cli("unknown_op", ["5"], registry, calc)
        captured = capsys.readouterr()
        assert result == 1
        assert "Error:" in captured.err
        assert "unknown_op" in captured.err

    def test_execute_cli_missing_operand(self, capsys, calc_and_registry):
        """Test binary op with missing second operand returns 1."""
        calc, registry = calc_and_registry
        result = execute_cli("add", ["5"], registry, calc)
        captured = capsys.readouterr()
        assert result == 1
        assert "Error:" in captured.err
        assert "expects 2" in captured.err

    def test_execute_cli_extra_operands(self, capsys, calc_and_registry):
        """Test unary op with extra operand returns 1."""
        calc, registry = calc_and_registry
        result = execute_cli("factorial", ["5", "3"], registry, calc)
        captured = capsys.readouterr()
        assert result == 1
        assert "Error:" in captured.err
        assert "expects 1" in captured.err

    def test_execute_cli_non_numeric_operand(self, capsys, calc_and_registry):
        """Test non-numeric operand returns 1."""
        calc, registry = calc_and_registry
        result = execute_cli("add", ["5", "abc"], registry, calc)
        captured = capsys.readouterr()
        assert result == 1
        assert "Error:" in captured.err
        assert "not a valid number" in captured.err

    def test_execute_cli_divide_by_zero(self, capsys, calc_and_registry):
        """Test division by zero returns 1."""
        calc, registry = calc_and_registry
        result = execute_cli("divide", ["10", "0"], registry, calc)
        captured = capsys.readouterr()
        assert result == 1
        assert "Error:" in captured.err

    def test_execute_cli_factorial_negative(self, capsys, calc_and_registry):
        """Test factorial with negative number returns 1."""
        calc, registry = calc_and_registry
        result = execute_cli("factorial", ["-5"], registry, calc)
        captured = capsys.readouterr()
        assert result == 1
        assert "Error:" in captured.err

    def test_execute_cli_sqrt_negative(self, capsys, calc_and_registry):
        """Test square_root with negative number returns 1."""
        calc, registry = calc_and_registry
        result = execute_cli("square_root", ["-4"], registry, calc)
        captured = capsys.readouterr()
        assert result == 1
        assert "Error:" in captured.err

    def test_execute_cli_log_non_positive(self, capsys, calc_and_registry):
        """Test log with non-positive number returns 1."""
        calc, registry = calc_and_registry
        result = execute_cli("log", ["0"], registry, calc)
        captured = capsys.readouterr()
        assert result == 1
        assert "Error:" in captured.err

    def test_execute_cli_ln_non_positive(self, capsys, calc_and_registry):
        """Test ln with non-positive number returns 1."""
        calc, registry = calc_and_registry
        result = execute_cli("ln", ["-1"], registry, calc)
        captured = capsys.readouterr()
        assert result == 1
        assert "Error:" in captured.err

    def test_execute_cli_no_operands_for_binary(self, capsys, calc_and_registry):
        """Test binary op with no operands returns 1."""
        calc, registry = calc_and_registry
        result = execute_cli("add", [], registry, calc)
        captured = capsys.readouterr()
        assert result == 1
        assert "Error:" in captured.err

    def test_execute_cli_factorial_float_operand(self, capsys, calc_and_registry):
        """Test factorial with float operand returns 1."""
        calc, registry = calc_and_registry
        result = execute_cli("factorial", ["5.5"], registry, calc)
        captured = capsys.readouterr()
        assert result == 1
        assert "Error:" in captured.err

    def test_execute_cli_power_negative_base_non_integer_exponent(
        self, capsys, calc_and_registry
    ):
        """Test power with negative base and non-integer exponent returns 1."""
        calc, registry = calc_and_registry
        result = execute_cli("power", ["-2", "0.5"], registry, calc)
        captured = capsys.readouterr()
        assert result == 1
        assert "Error:" in captured.err

    def test_execute_cli_multiple_non_numeric_operands(
        self, capsys, calc_and_registry
    ):
        """Test that only first non-numeric operand is reported."""
        calc, registry = calc_and_registry
        result = execute_cli("add", ["abc", "def"], registry, calc)
        captured = capsys.readouterr()
        assert result == 1
        assert "Error:" in captured.err
        assert "abc" in captured.err


# ==================== Integration Tests (subprocess) ====================

class TestMainPyIntegration:
    """Integration tests running main.py as a subprocess."""

    @pytest.fixture
    def repo_root(self):
        """Fixture to get the repository root directory."""
        return Path(__file__).parent.parent

    def test_main_py_add_success(self, repo_root):
        """Test main.py with valid add operation."""
        result = subprocess.run(
            [sys.executable, "main.py", "add", "5", "3"],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "8" in result.stdout

    def test_main_py_factorial_success(self, repo_root):
        """Test main.py with valid factorial operation."""
        result = subprocess.run(
            [sys.executable, "main.py", "factorial", "5"],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "120" in result.stdout

    def test_main_py_subtract_success(self, repo_root):
        """Test main.py with subtract operation."""
        result = subprocess.run(
            [sys.executable, "main.py", "subtract", "10", "3"],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "7" in result.stdout

    def test_main_py_square_root_success(self, repo_root):
        """Test main.py with square_root operation."""
        result = subprocess.run(
            [sys.executable, "main.py", "square_root", "9"],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "3" in result.stdout

    def test_main_py_no_args(self, repo_root):
        """Test main.py with no arguments."""
        result = subprocess.run(
            [sys.executable, "main.py"],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
        assert "Usage:" in result.stderr

    def test_main_py_invalid_operation(self, repo_root):
        """Test main.py with invalid operation."""
        result = subprocess.run(
            [sys.executable, "main.py", "invalid_op", "5"],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
        assert "Error:" in result.stderr

    def test_main_py_missing_operand(self, repo_root):
        """Test main.py with missing operand for binary operation."""
        result = subprocess.run(
            [sys.executable, "main.py", "add", "5"],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
        assert "Error:" in result.stderr

    def test_main_py_non_numeric_operand(self, repo_root):
        """Test main.py with non-numeric operand."""
        result = subprocess.run(
            [sys.executable, "main.py", "add", "5", "abc"],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
        assert "Error:" in result.stderr

    def test_main_py_divide_by_zero(self, repo_root):
        """Test main.py with division by zero."""
        result = subprocess.run(
            [sys.executable, "main.py", "divide", "10", "0"],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
        assert "Error:" in result.stderr

    def test_main_py_multiply_success(self, repo_root):
        """Test main.py with multiply operation."""
        result = subprocess.run(
            [sys.executable, "main.py", "multiply", "4", "5"],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "20" in result.stdout

    def test_main_py_power_success(self, repo_root):
        """Test main.py with power operation."""
        result = subprocess.run(
            [sys.executable, "main.py", "power", "2", "10"],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "1024" in result.stdout

    def test_main_py_log_success(self, repo_root):
        """Test main.py with log operation."""
        result = subprocess.run(
            [sys.executable, "main.py", "log", "100"],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "2" in result.stdout

    def test_main_py_negative_numbers(self, repo_root):
        """Test main.py with negative operands."""
        result = subprocess.run(
            [sys.executable, "main.py", "add", "-5", "3"],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "-2" in result.stdout

    def test_main_py_float_operands(self, repo_root):
        """Test main.py with float operands."""
        result = subprocess.run(
            [sys.executable, "main.py", "add", "2.5", "1.5"],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "4" in result.stdout
