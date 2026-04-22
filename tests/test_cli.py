"""Comprehensive pytest tests for the CLI module."""

import pytest
import sys
from io import StringIO

from src.cli import parse_args, execute_cli, cli_main


class TestCLIArgumentParsing:
    """Tests for parse_args function."""

    def test_parse_args_add_two_operands(self):
        """parse_args should handle basic two-operand operations."""
        operation, operands = parse_args(["add", "2", "3"])
        assert operation == "add"
        assert operands == [2.0, 3.0]

    def test_parse_args_subtract_two_operands(self):
        """parse_args should handle subtraction with two operands."""
        operation, operands = parse_args(["subtract", "5", "3"])
        assert operation == "subtract"
        assert operands == [5.0, 3.0]

    def test_parse_args_single_operand_operation(self):
        """parse_args should handle single-operand operations like factorial."""
        operation, operands = parse_args(["factorial", "5"])
        assert operation == "factorial"
        assert operands == [5.0]

    @pytest.mark.parametrize(
        "argv,expected_operation,expected_operands",
        [
            (["add", "1.5", "2.5"], "add", [1.5, 2.5]),
            (["multiply", "3.7", "2.1"], "multiply", [3.7, 2.1]),
            (["square_root", "16.0"], "square_root", [16.0]),
        ],
    )
    def test_parse_args_decimal_operands(
        self, argv, expected_operation, expected_operands
    ):
        """parse_args should handle decimal operands."""
        operation, operands = parse_args(argv)
        assert operation == expected_operation
        assert operands == expected_operands

    @pytest.mark.parametrize(
        "argv,expected_operation,expected_operands",
        [
            (["subtract", "-5", "3"], "subtract", [-5.0, 3.0]),
            (["add", "-10", "-20"], "add", [-10.0, -20.0]),
            (["divide", "-8", "2"], "divide", [-8.0, 2.0]),
        ],
    )
    def test_parse_args_negative_operands(
        self, argv, expected_operation, expected_operands
    ):
        """parse_args should handle negative operands."""
        operation, operands = parse_args(argv)
        assert operation == expected_operation
        assert operands == expected_operands

    @pytest.mark.parametrize(
        "argv",
        [
            (["factorial", "20"],),
            (["factorial", "100"],),
        ],
    )
    def test_parse_args_large_number(self, argv):
        """parse_args should handle large numbers."""
        operation, operands = parse_args(argv[0])
        assert operation == "factorial"
        assert operands == [float(argv[0][1])]

    def test_parse_args_missing_operation_empty_list(self):
        """parse_args should raise SystemExit when argv is empty."""
        with pytest.raises(SystemExit) as exc_info:
            parse_args([])
        assert exc_info.value.code == 1

    @pytest.mark.parametrize(
        "argv",
        [
            (["add", "2", "abc"],),
            (["multiply", "3", "xyz"],),
            (["divide", "abc", "2"],),
        ],
    )
    def test_parse_args_non_numeric_operand(self, argv):
        """parse_args should raise ValueError for non-numeric operands."""
        with pytest.raises(ValueError, match="Invalid numeric operand"):
            parse_args(argv[0])


class TestCLIExecution:
    """Tests for execute_cli function."""

    @pytest.mark.parametrize(
        "operation,operands,expected",
        [
            ("add", [2.0, 3.0], 5.0),
            ("add", [10.0, 20.0], 30.0),
            ("add", [-5.0, 3.0], -2.0),
        ],
    )
    def test_execute_cli_add(self, operation, operands, expected):
        """execute_cli should correctly add two operands."""
        result = execute_cli(operation, operands)
        assert result == expected

    @pytest.mark.parametrize(
        "operation,operands,expected",
        [
            ("subtract", [10.0, 3.0], 7.0),
            ("subtract", [5.0, 5.0], 0.0),
            ("subtract", [3.0, 10.0], -7.0),
        ],
    )
    def test_execute_cli_subtract(self, operation, operands, expected):
        """execute_cli should correctly subtract operands."""
        result = execute_cli(operation, operands)
        assert result == expected

    @pytest.mark.parametrize(
        "operation,operands,expected",
        [
            ("multiply", [4.0, 5.0], 20.0),
            ("multiply", [0.0, 100.0], 0.0),
            ("multiply", [-3.0, 4.0], -12.0),
        ],
    )
    def test_execute_cli_multiply(self, operation, operands, expected):
        """execute_cli should correctly multiply operands."""
        result = execute_cli(operation, operands)
        assert result == expected

    @pytest.mark.parametrize(
        "operation,operands,expected",
        [
            ("divide", [10.0, 2.0], 5.0),
            ("divide", [7.0, 2.0], 3.5),
            ("divide", [1.0, 4.0], 0.25),
        ],
    )
    def test_execute_cli_divide(self, operation, operands, expected):
        """execute_cli should correctly divide operands."""
        result = execute_cli(operation, operands)
        assert result == expected

    def test_execute_cli_divide_by_zero(self):
        """execute_cli should raise ZeroDivisionError for division by zero."""
        with pytest.raises(ZeroDivisionError):
            execute_cli("divide", [5.0, 0.0])

    @pytest.mark.parametrize(
        "operation,operands,expected",
        [
            ("factorial", [5.0], 120),
            ("factorial", [0.0], 1),
            ("factorial", [1.0], 1),
            ("factorial", [10.0], 3628800),
        ],
    )
    def test_execute_cli_factorial(self, operation, operands, expected):
        """execute_cli should correctly compute factorial."""
        result = execute_cli(operation, operands)
        assert result == expected

    @pytest.mark.parametrize(
        "operation,operands,expected",
        [
            ("square", [3.0], 9.0),
            ("square", [0.0], 0.0),
            ("square", [-4.0], 16.0),
        ],
    )
    def test_execute_cli_square(self, operation, operands, expected):
        """execute_cli should correctly square a value."""
        result = execute_cli(operation, operands)
        assert result == expected

    @pytest.mark.parametrize(
        "operation,operands,expected",
        [
            ("square_root", [9.0], 3.0),
            ("square_root", [0.0], 0.0),
            ("square_root", [16.0], 4.0),
        ],
    )
    def test_execute_cli_square_root(self, operation, operands, expected):
        """execute_cli should correctly compute square root."""
        result = execute_cli(operation, operands)
        assert result == expected

    def test_execute_cli_square_root_negative(self):
        """execute_cli should raise ValueError for square root of negative."""
        with pytest.raises(ValueError, match="Square root is not defined"):
            execute_cli("square_root", [-1.0])

    def test_execute_cli_unknown_operation(self):
        """execute_cli should raise KeyError for unknown operation."""
        with pytest.raises(KeyError, match="Unknown operation"):
            execute_cli("foo", [2.0])

    def test_execute_cli_wrong_arity_too_few(self):
        """execute_cli should raise ValueError for missing operand."""
        with pytest.raises(ValueError, match="expects 2 operand"):
            execute_cli("add", [2.0])

    def test_execute_cli_wrong_arity_too_many(self):
        """execute_cli should raise ValueError for extra operand."""
        with pytest.raises(ValueError, match="expects 2 operand"):
            execute_cli("add", [2.0, 3.0, 4.0])

    def test_execute_cli_factorial_wrong_arity(self):
        """execute_cli should raise ValueError for factorial with multiple operands."""
        with pytest.raises(ValueError, match="expects 1 operand"):
            execute_cli("factorial", [5.0, 3.0])


class TestCLIMainIntegration:
    """Integration tests for cli_main function using capsys fixture."""

    def test_cli_main_success_add(self, capsys):
        """cli_main should print result and exit 0 for successful addition."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["add", "2", "3"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert captured.out == "5\n"
        assert captured.err == ""

    def test_cli_main_success_divide_float(self, capsys):
        """cli_main should print float result correctly."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["divide", "7", "2"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert captured.out == "3.5\n"
        assert captured.err == ""

    def test_cli_main_success_factorial(self, capsys):
        """cli_main should print factorial result as integer."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["factorial", "5"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert captured.out == "120\n"
        assert captured.err == ""

    def test_cli_main_success_negative_operand(self, capsys):
        """cli_main should handle negative operands correctly."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["add", "-5", "3"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert captured.out == "-2\n"
        assert captured.err == ""

    def test_cli_main_unknown_operation_exit_1(self, capsys):
        """cli_main should exit 1 and print error for unknown operation."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["foo", "2", "3"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err
        assert captured.out == ""

    def test_cli_main_non_numeric_operand_exit_1(self, capsys):
        """cli_main should exit 1 and print error for non-numeric operand."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["add", "2", "abc"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err
        assert captured.out == ""

    def test_cli_main_divide_by_zero_exit_1(self, capsys):
        """cli_main should exit 1 and print error for division by zero."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["divide", "5", "0"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err
        assert captured.out == ""

    def test_cli_main_missing_args_exit_1(self, capsys):
        """cli_main should exit 1 when argv is empty."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main([])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_cli_main_wrong_arity_exit_1(self, capsys):
        """cli_main should exit 1 and print error for wrong arity."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["add", "2"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err
        assert captured.out == ""

    def test_cli_main_error_nothing_on_stdout(self, capsys):
        """cli_main should not print anything to stdout on error."""
        with pytest.raises(SystemExit):
            cli_main(["unknown_operation", "1", "2"])
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_cli_main_large_result(self, capsys):
        """cli_main should handle large results correctly."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["factorial", "10"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert captured.out == "3628800\n"
        assert captured.err == ""

    def test_cli_main_square_root(self, capsys):
        """cli_main should strip .0 suffix for whole-number square root."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["square_root", "9"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert captured.out == "3\n"
        assert captured.err == ""

    def test_cli_main_sqrt_negative_exit_1(self, capsys):
        """cli_main should exit 1 for square root of negative number."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["square_root", "-1"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err
        assert captured.out == ""

    def test_cli_main_multiply_decimal_result(self, capsys):
        """cli_main should handle decimal multiplication results."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["multiply", "2.5", "3"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert captured.out == "7.5\n"
        assert captured.err == ""

    def test_cli_main_subtract_negative_result(self, capsys):
        """cli_main should handle negative results correctly."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["subtract", "2", "5"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert captured.out == "-3\n"
        assert captured.err == ""

    def test_cli_main_cube(self, capsys):
        """cli_main should correctly compute cube."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["cube", "2"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert captured.out == "8\n"
        assert captured.err == ""

    def test_cli_main_cube_root(self, capsys):
        """cli_main should correctly compute cube root."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["cube_root", "8"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert captured.out == "2\n"
        assert captured.err == ""

    def test_cli_main_power(self, capsys):
        """cli_main should correctly compute power."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["power", "2", "8"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert captured.out == "256\n"
        assert captured.err == ""

    def test_cli_main_log(self, capsys):
        """cli_main should correctly compute base-10 logarithm."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["log", "100"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert captured.out == "2\n"
        assert captured.err == ""

    def test_cli_main_ln(self, capsys):
        """cli_main should correctly compute natural logarithm."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["ln", "2.718281828"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        # Natural log of e should be approximately 1
        assert "1" in captured.out
        assert captured.err == ""
