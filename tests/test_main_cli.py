"""Test suite for the main.py CLI entry point.

Tests cover success paths for all operations, error handling, edge cases,
operand validation, and internal utility functions.
"""

import subprocess
import sys
import math
import pytest

from src.calculator import Calculator
from main import (
    get_operation_arity,
    parse_arguments,
    _to_number,
    execute_operation,
)


# ============================================================================
# Subprocess-based CLI Tests
# ============================================================================

class TestCLIBasicTwoOperandOperations:
    """Test successful execution of two-operand operations via CLI."""

    @pytest.fixture
    def run_cli(self):
        """Helper to run main.py as a subprocess from project root."""
        def _run(*args):
            cmd = [sys.executable, "main.py"] + list(args)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        return _run

    def test_cli_add_two_positive_integers(self, run_cli):
        """Test: add 5 7 -> stdout '12', exit 0."""
        stdout, stderr, returncode = run_cli("add", "5", "7")
        assert returncode == 0
        assert stdout == "12"
        assert stderr == ""

    def test_cli_add_with_floats(self, run_cli):
        """Test: add 3.5 2.5 -> stdout '6.0', exit 0."""
        stdout, stderr, returncode = run_cli("add", "3.5", "2.5")
        assert returncode == 0
        assert stdout == "6.0"
        assert stderr == ""

    def test_cli_subtract(self, run_cli):
        """Test: subtract 10 3 -> stdout '7', exit 0."""
        stdout, stderr, returncode = run_cli("subtract", "10", "3")
        assert returncode == 0
        assert stdout == "7"
        assert stderr == ""

    def test_cli_multiply(self, run_cli):
        """Test: multiply 4 5 -> stdout '20', exit 0."""
        stdout, stderr, returncode = run_cli("multiply", "4", "5")
        assert returncode == 0
        assert stdout == "20"
        assert stderr == ""

    def test_cli_divide(self, run_cli):
        """Test: divide 10 2 -> stdout '5.0', exit 0."""
        stdout, stderr, returncode = run_cli("divide", "10", "2")
        assert returncode == 0
        assert stdout == "5.0"
        assert stderr == ""

    def test_cli_power(self, run_cli):
        """Test: power 2 3 -> stdout '8.0', exit 0."""
        stdout, stderr, returncode = run_cli("power", "2", "3")
        assert returncode == 0
        assert stdout == "8.0"
        assert stderr == ""

    @pytest.mark.parametrize("op,a,b,expected", [
        ("add", "1", "1", "2"),
        ("add", "-5", "10", "5"),
        ("subtract", "5", "5", "0"),
        ("subtract", "-2", "-1", "-1"),
        ("multiply", "0", "100", "0"),
        ("multiply", "-3", "-4", "12"),
        ("divide", "1", "2", "0.5"),
        ("divide", "-10", "2", "-5.0"),
        ("power", "10", "0", "1.0"),
    ])
    def test_cli_two_operand_operations_parametrized(self, run_cli, op, a, b, expected):
        """Parametrized tests for various two-operand operation inputs."""
        stdout, stderr, returncode = run_cli(op, a, b)
        assert returncode == 0
        assert stdout == expected
        assert stderr == ""


class TestCLIBasicOneOperandOperations:
    """Test successful execution of one-operand operations via CLI."""

    @pytest.fixture
    def run_cli(self):
        """Helper to run main.py as a subprocess."""
        def _run(*args):
            cmd = [sys.executable, "main.py"] + list(args)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        return _run

    def test_cli_factorial(self, run_cli):
        """Test: factorial 5 -> stdout '120', exit 0."""
        stdout, stderr, returncode = run_cli("factorial", "5")
        assert returncode == 0
        assert stdout == "120"
        assert stderr == ""

    def test_cli_square(self, run_cli):
        """Test: square 4 -> stdout '16.0', exit 0."""
        stdout, stderr, returncode = run_cli("square", "4")
        assert returncode == 0
        assert stdout == "16.0"
        assert stderr == ""

    def test_cli_cube(self, run_cli):
        """Test: cube 3 -> stdout '27.0', exit 0."""
        stdout, stderr, returncode = run_cli("cube", "3")
        assert returncode == 0
        assert stdout == "27.0"
        assert stderr == ""

    def test_cli_square_root(self, run_cli):
        """Test: square_root 16 -> stdout '4.0', exit 0."""
        stdout, stderr, returncode = run_cli("square_root", "16")
        assert returncode == 0
        assert stdout == "4.0"
        assert stderr == ""

    def test_cli_cube_root(self, run_cli):
        """Test: cube_root 8 -> stdout '2.0', exit 0."""
        stdout, stderr, returncode = run_cli("cube_root", "8")
        assert returncode == 0
        assert stdout == "2.0"
        assert stderr == ""

    def test_cli_logarithm(self, run_cli):
        """Test: logarithm 100 -> stdout approx '2.0', exit 0."""
        stdout, stderr, returncode = run_cli("logarithm", "100")
        assert returncode == 0
        assert stderr == ""
        # log10(100) = 2.0
        result = float(stdout)
        assert math.isclose(result, 2.0, rel_tol=1e-9)

    def test_cli_natural_logarithm(self, run_cli):
        """Test: natural_logarithm 1 -> stdout '0.0', exit 0."""
        stdout, stderr, returncode = run_cli("natural_logarithm", "1")
        assert returncode == 0
        assert stdout == "0.0"
        assert stderr == ""

    @pytest.mark.parametrize("op,x,expected_approx", [
        ("factorial", "0", 1),
        ("factorial", "3", 6),
        ("square", "5", 25.0),
        ("square", "-3", 9.0),
        ("cube", "2", 8.0),
        ("cube", "-2", -8.0),
        ("square_root", "9", 3.0),
        ("square_root", "0.25", 0.5),
        ("cube_root", "27", 3.0),
        ("cube_root", "-8", -2.0),
        ("natural_logarithm", "2.718281828", 1.0),
    ])
    def test_cli_one_operand_operations_parametrized(self, run_cli, op, x, expected_approx):
        """Parametrized tests for various one-operand operation inputs."""
        stdout, stderr, returncode = run_cli(op, x)
        assert returncode == 0
        assert stderr == ""
        result = float(stdout)
        assert math.isclose(result, expected_approx, rel_tol=1e-6)


class TestCLIMissingOperands:
    """Test error handling for missing operands."""

    @pytest.fixture
    def run_cli(self):
        """Helper to run main.py as a subprocess."""
        def _run(*args):
            cmd = [sys.executable, "main.py"] + list(args)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        return _run

    def test_cli_no_arguments(self, run_cli):
        """Test: no arguments -> stderr with usage message, exit 1."""
        stdout, stderr, returncode = run_cli()
        assert returncode == 1
        assert "Error" in stderr or "Usage" in stderr
        assert stdout == ""

    def test_cli_two_operand_missing_both_operands(self, run_cli):
        """Test: add (no operands) -> stderr 'Error', exit 1."""
        stdout, stderr, returncode = run_cli("add")
        assert returncode == 1
        assert "Error" in stderr
        assert stdout == ""

    def test_cli_two_operand_missing_second_operand(self, run_cli):
        """Test: add 5 (missing second) -> stderr 'Error', exit 1."""
        stdout, stderr, returncode = run_cli("add", "5")
        assert returncode == 1
        assert "Error" in stderr
        assert stdout == ""

    def test_cli_one_operand_missing_operand(self, run_cli):
        """Test: factorial (no operand) -> stderr 'Error', exit 1."""
        stdout, stderr, returncode = run_cli("factorial")
        assert returncode == 1
        assert "Error" in stderr
        assert stdout == ""

    @pytest.mark.parametrize("op", ["add", "subtract", "multiply", "divide", "power"])
    def test_cli_two_operand_missing_both(self, run_cli, op):
        """Parametrized: all two-operand ops without operands should fail."""
        stdout, stderr, returncode = run_cli(op)
        assert returncode == 1
        assert "Error" in stderr
        assert stdout == ""

    @pytest.mark.parametrize("op", ["factorial", "square", "cube", "square_root", "cube_root", "logarithm", "natural_logarithm"])
    def test_cli_one_operand_missing(self, run_cli, op):
        """Parametrized: all one-operand ops without operand should fail."""
        stdout, stderr, returncode = run_cli(op)
        assert returncode == 1
        assert "Error" in stderr
        assert stdout == ""


class TestCLIInvalidOperationName:
    """Test error handling for invalid operation names."""

    @pytest.fixture
    def run_cli(self):
        """Helper to run main.py as a subprocess."""
        def _run(*args):
            cmd = [sys.executable, "main.py"] + list(args)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        return _run

    def test_cli_unknown_operation(self, run_cli):
        """Test: unknown_op 5 3 -> stderr 'unknown operation', exit 1."""
        stdout, stderr, returncode = run_cli("unknown_op", "5", "3")
        assert returncode == 1
        assert "Error" in stderr
        assert "unknown operation" in stderr
        assert stdout == ""

    @pytest.mark.parametrize("invalid_op", [
        "foobar",
        "add_extra",
        "_private",
        "nonexistent",
        "FACTORIAL",
    ])
    def test_cli_various_unknown_operations(self, run_cli, invalid_op):
        """Parametrized: various invalid operation names should fail."""
        stdout, stderr, returncode = run_cli(invalid_op, "5")
        assert returncode == 1
        assert "Error" in stderr
        assert stdout == ""


class TestCLIExcessOperands:
    """Test that excess operands are silently trimmed."""

    @pytest.fixture
    def run_cli(self):
        """Helper to run main.py as a subprocess."""
        def _run(*args):
            cmd = [sys.executable, "main.py"] + list(args)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        return _run

    def test_cli_two_operand_with_excess_operands(self, run_cli):
        """Test: add 5 3 99 -> succeeds, result 8 (extra trimmed), exit 0."""
        stdout, stderr, returncode = run_cli("add", "5", "3", "99")
        assert returncode == 0
        assert stdout == "8"
        assert stderr == ""

    def test_cli_one_operand_with_excess_operands(self, run_cli):
        """Test: factorial 5 3 -> succeeds, result 120 (extra trimmed), exit 0."""
        stdout, stderr, returncode = run_cli("factorial", "5", "3")
        assert returncode == 0
        assert stdout == "120"
        assert stderr == ""

    @pytest.mark.parametrize("op,args,expected", [
        ("subtract", ["10", "3", "5", "100"], "7"),
        ("multiply", ["4", "5", "10"], "20"),
        ("divide", ["10", "2", "5"], "5.0"),
        ("square", ["4", "999"], "16.0"),
        ("cube", ["3", "1", "2"], "27.0"),
    ])
    def test_cli_excess_operands_parametrized(self, run_cli, op, args, expected):
        """Parametrized: excess operands are trimmed for various operations."""
        stdout, stderr, returncode = run_cli(op, *args)
        assert returncode == 0
        assert stdout == expected
        assert stderr == ""


class TestCLIInvalidOperandTypes:
    """Test error handling for non-numeric operands."""

    @pytest.fixture
    def run_cli(self):
        """Helper to run main.py as a subprocess."""
        def _run(*args):
            cmd = [sys.executable, "main.py"] + list(args)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        return _run

    def test_cli_non_numeric_operand_for_two_operand(self, run_cli):
        """Test: add 5 abc -> stderr 'Error', exit 1."""
        stdout, stderr, returncode = run_cli("add", "5", "abc")
        assert returncode == 1
        assert "Error" in stderr
        assert stdout == ""

    def test_cli_non_numeric_operand_for_one_operand(self, run_cli):
        """Test: square abc -> stderr 'Error', exit 1."""
        stdout, stderr, returncode = run_cli("square", "abc")
        assert returncode == 1
        assert "Error" in stderr
        assert stdout == ""

    @pytest.mark.parametrize("invalid_operand", [
        "abc",
        "12.34.56",
        "1e2e3",
        "",
    ])
    def test_cli_invalid_operand_types_parametrized(self, run_cli, invalid_operand):
        """Parametrized: various invalid operand types should fail."""
        stdout, stderr, returncode = run_cli("add", "5", invalid_operand)
        assert returncode == 1
        assert "Error" in stderr
        assert stdout == ""


class TestCLICalculatorErrors:
    """Test error handling for calculator-level errors."""

    @pytest.fixture
    def run_cli(self):
        """Helper to run main.py as a subprocess."""
        def _run(*args):
            cmd = [sys.executable, "main.py"] + list(args)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        return _run

    def test_cli_division_by_zero(self, run_cli):
        """Test: divide 5 0 -> stderr 'Error', exit 1."""
        stdout, stderr, returncode = run_cli("divide", "5", "0")
        assert returncode == 1
        assert "Error" in stderr
        assert stdout == ""

    def test_cli_factorial_negative(self, run_cli):
        """Test: factorial -5 -> stderr 'Error', exit 1."""
        stdout, stderr, returncode = run_cli("factorial", "-5")
        assert returncode == 1
        assert "Error" in stderr
        assert stdout == ""

    def test_cli_square_root_negative(self, run_cli):
        """Test: square_root -4 -> stderr 'Error', exit 1."""
        stdout, stderr, returncode = run_cli("square_root", "-4")
        assert returncode == 1
        assert "Error" in stderr
        assert stdout == ""

    def test_cli_logarithm_zero(self, run_cli):
        """Test: logarithm 0 -> stderr 'Error', exit 1."""
        stdout, stderr, returncode = run_cli("logarithm", "0")
        assert returncode == 1
        assert "Error" in stderr
        assert stdout == ""

    def test_cli_logarithm_negative(self, run_cli):
        """Test: logarithm -5 -> stderr 'Error', exit 1."""
        stdout, stderr, returncode = run_cli("logarithm", "-5")
        assert returncode == 1
        assert "Error" in stderr
        assert stdout == ""

    def test_cli_natural_logarithm_zero(self, run_cli):
        """Test: natural_logarithm 0 -> stderr 'Error', exit 1."""
        stdout, stderr, returncode = run_cli("natural_logarithm", "0")
        assert returncode == 1
        assert "Error" in stderr
        assert stdout == ""

    def test_cli_natural_logarithm_negative(self, run_cli):
        """Test: natural_logarithm -1 -> stderr 'Error', exit 1."""
        stdout, stderr, returncode = run_cli("natural_logarithm", "-1")
        assert returncode == 1
        assert "Error" in stderr
        assert stdout == ""


class TestCLIOutputFormat:
    """Test output stream handling (stdout/stderr separation)."""

    @pytest.fixture
    def run_cli(self):
        """Helper to run main.py as a subprocess."""
        def _run(*args):
            cmd = [sys.executable, "main.py"] + list(args)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        return _run

    def test_cli_result_on_stdout_only(self, run_cli):
        """Test: valid operation prints result on stdout, stderr empty."""
        stdout, stderr, returncode = run_cli("add", "5", "3")
        assert returncode == 0
        assert stdout == "8"
        assert stderr == ""

    def test_cli_error_on_stderr_not_stdout(self, run_cli):
        """Test: error goes to stderr, stdout empty."""
        stdout, stderr, returncode = run_cli("add", "5", "abc")
        assert returncode == 1
        assert stdout == ""
        assert "Error" in stderr

    def test_cli_exit_code_success(self, run_cli):
        """Test: valid operation exits with code 0."""
        stdout, stderr, returncode = run_cli("multiply", "2", "3")
        assert returncode == 0

    def test_cli_exit_code_failure(self, run_cli):
        """Test: invalid operation exits with code 1."""
        stdout, stderr, returncode = run_cli("invalid", "1", "2")
        assert returncode == 1


class TestCLIConsistencyWithCalculator:
    """Test that CLI results match direct Calculator method calls."""

    @pytest.fixture
    def run_cli(self):
        """Helper to run main.py as a subprocess."""
        def _run(*args):
            cmd = [sys.executable, "main.py"] + list(args)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        return _run

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance."""
        return Calculator()

    def test_cli_add_matches_direct_calculator(self, run_cli, calculator):
        """Test: CLI add result matches Calculator.add()."""
        stdout, stderr, returncode = run_cli("add", "5", "7")
        assert returncode == 0
        cli_result = float(stdout)
        direct_result = calculator.add(5, 7)
        assert cli_result == direct_result

    def test_cli_factorial_matches_direct_calculator(self, run_cli, calculator):
        """Test: CLI factorial result matches Calculator.factorial()."""
        stdout, stderr, returncode = run_cli("factorial", "5")
        assert returncode == 0
        cli_result = float(stdout)
        direct_result = calculator.factorial(5)
        assert cli_result == direct_result

    def test_cli_square_root_matches_direct_calculator(self, run_cli, calculator):
        """Test: CLI square_root result matches Calculator.square_root()."""
        stdout, stderr, returncode = run_cli("square_root", "16")
        assert returncode == 0
        cli_result = float(stdout)
        direct_result = calculator.square_root(16)
        assert math.isclose(cli_result, direct_result, rel_tol=1e-9)

    def test_cli_divide_matches_direct_calculator(self, run_cli, calculator):
        """Test: CLI divide result matches Calculator.divide()."""
        stdout, stderr, returncode = run_cli("divide", "10", "2")
        assert returncode == 0
        cli_result = float(stdout)
        direct_result = calculator.divide(10, 2)
        assert cli_result == direct_result


# ============================================================================
# Unit Tests for Internal Functions
# ============================================================================

class TestGetOperationArity:
    """Unit tests for get_operation_arity() function."""

    @pytest.mark.parametrize("operation,expected_arity", [
        ("add", 2),
        ("subtract", 2),
        ("multiply", 2),
        ("divide", 2),
        ("power", 2),
    ])
    def test_get_operation_arity_two_operand_operations(self, operation, expected_arity):
        """Test that two-operand operations return arity 2."""
        assert get_operation_arity(operation) == expected_arity

    @pytest.mark.parametrize("operation,expected_arity", [
        ("factorial", 1),
        ("square", 1),
        ("cube", 1),
        ("square_root", 1),
        ("cube_root", 1),
        ("logarithm", 1),
        ("natural_logarithm", 1),
    ])
    def test_get_operation_arity_one_operand_operations(self, operation, expected_arity):
        """Test that one-operand operations return arity 1."""
        assert get_operation_arity(operation) == expected_arity

    @pytest.mark.parametrize("operation", [
        "unknown",
        "foobar",
        "add_extra",
        "_private",
        "nonexistent",
    ])
    def test_get_operation_arity_unknown_returns_minus_one(self, operation):
        """Test that unknown operations return -1."""
        assert get_operation_arity(operation) == -1

    def test_get_operation_arity_case_sensitive(self):
        """Test that operation names are case-sensitive."""
        assert get_operation_arity("add") == 2
        assert get_operation_arity("ADD") == -1
        assert get_operation_arity("Add") == -1


class TestParseArguments:
    """Unit tests for parse_arguments() function."""

    def test_parse_arguments_normal(self):
        """Test: parse_arguments(['add', '5', '7']) -> ('add', ['5', '7'])."""
        operation, operands = parse_arguments(["add", "5", "7"])
        assert operation == "add"
        assert operands == ["5", "7"]

    def test_parse_arguments_single_operand(self):
        """Test: single operand is parsed correctly."""
        operation, operands = parse_arguments(["factorial", "5"])
        assert operation == "factorial"
        assert operands == ["5"]

    def test_parse_arguments_no_operands(self):
        """Test: operation with no operands."""
        operation, operands = parse_arguments(["add"])
        assert operation == "add"
        assert operands == []

    def test_parse_arguments_many_operands(self):
        """Test: many operands are all returned."""
        operation, operands = parse_arguments(["op", "1", "2", "3", "4", "5"])
        assert operation == "op"
        assert operands == ["1", "2", "3", "4", "5"]

    def test_parse_arguments_empty_list_raises_system_exit(self):
        """Test: empty argument list calls sys.exit(1)."""
        with pytest.raises(SystemExit) as exc_info:
            parse_arguments([])
        assert exc_info.value.code == 1

    def test_parse_arguments_preserves_operand_strings(self):
        """Test: operand strings are not modified."""
        operation, operands = parse_arguments(["add", "3.5", "-10", "1e-3"])
        assert operands == ["3.5", "-10", "1e-3"]


class TestToNumber:
    """Unit tests for _to_number() function."""

    @pytest.mark.parametrize("value,expected", [
        ("5", 5),
        ("0", 0),
        ("-10", -10),
        ("999999", 999999),
    ])
    def test_to_number_integer_strings(self, value, expected):
        """Test: integer strings are converted to int."""
        result = _to_number(value)
        assert result == expected
        assert isinstance(result, int)

    @pytest.mark.parametrize("value,expected", [
        ("3.14", 3.14),
        ("0.5", 0.5),
        ("-2.5", -2.5),
        ("1.0", 1.0),
    ])
    def test_to_number_float_strings(self, value, expected):
        """Test: float strings are converted to float."""
        result = _to_number(value)
        assert result == expected
        assert isinstance(result, float)

    @pytest.mark.parametrize("value", [
        "1e10",
        "1e-5",
        "2.5e3",
        "-1.2e-4",
    ])
    def test_to_number_scientific_notation(self, value):
        """Test: scientific notation is parsed as float."""
        result = _to_number(value)
        assert isinstance(result, float)

    @pytest.mark.parametrize("invalid", [
        "abc",
        "1.2.3",
        "12a",
        "a12",
        "",
    ])
    def test_to_number_invalid_raises_value_error(self, invalid):
        """Test: invalid numeric strings raise ValueError."""
        with pytest.raises(ValueError):
            _to_number(invalid)

    def test_to_number_int_preferred_over_float(self):
        """Test: integer values return int type, not float."""
        result = _to_number("42")
        assert isinstance(result, int)
        assert result == 42


class TestExecuteOperation:
    """Unit tests for execute_operation() function."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance."""
        return Calculator()

    def test_execute_operation_two_operand_with_integers(self, calculator):
        """Test: execute_operation converts string '5', '7' and calls add."""
        result = execute_operation(calculator, "add", ["5", "7"])
        assert result == 12

    def test_execute_operation_one_operand_with_integer(self, calculator):
        """Test: execute_operation converts string '5' and calls factorial."""
        result = execute_operation(calculator, "factorial", ["5"])
        assert result == 120

    def test_execute_operation_with_floats(self, calculator):
        """Test: execute_operation handles float strings."""
        result = execute_operation(calculator, "add", ["3.5", "2.5"])
        assert result == 6.0

    def test_execute_operation_divide(self, calculator):
        """Test: execute_operation with divide."""
        result = execute_operation(calculator, "divide", ["10", "2"])
        assert result == 5.0

    def test_execute_operation_square_root(self, calculator):
        """Test: execute_operation with square_root."""
        result = execute_operation(calculator, "square_root", ["16"])
        assert math.isclose(result, 4.0)

    def test_execute_operation_invalid_operand_raises_value_error(self, calculator):
        """Test: invalid operand string raises ValueError."""
        with pytest.raises(ValueError):
            execute_operation(calculator, "add", ["5", "abc"])

    def test_execute_operation_division_by_zero_raises_error(self, calculator):
        """Test: division by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            execute_operation(calculator, "divide", ["5", "0"])

    def test_execute_operation_factorial_negative_raises_error(self, calculator):
        """Test: negative factorial raises ValueError."""
        with pytest.raises(ValueError):
            execute_operation(calculator, "factorial", ["-5"])

    def test_execute_operation_square_root_negative_raises_error(self, calculator):
        """Test: negative square_root raises ValueError."""
        with pytest.raises(ValueError):
            execute_operation(calculator, "square_root", ["-4"])

    def test_execute_operation_logarithm_non_positive_raises_error(self, calculator):
        """Test: non-positive logarithm raises ValueError."""
        with pytest.raises(ValueError):
            execute_operation(calculator, "logarithm", ["0"])

    @pytest.mark.parametrize("op,operands,should_raise", [
        ("add", ["5", "7"], None),
        ("subtract", ["-10", "3"], None),
        ("multiply", ["0", "100"], None),
        ("divide", ["10", "0"], ZeroDivisionError),
        ("factorial", ["-1"], ValueError),
        ("square_root", ["-1"], ValueError),
    ])
    def test_execute_operation_parametrized(self, calculator, op, operands, should_raise):
        """Parametrized: execute_operation with various inputs."""
        if should_raise:
            with pytest.raises(should_raise):
                execute_operation(calculator, op, operands)
        else:
            result = execute_operation(calculator, op, operands)
            assert isinstance(result, (int, float))
