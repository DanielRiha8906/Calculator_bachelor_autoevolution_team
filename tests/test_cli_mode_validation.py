"""Unit tests for CLI mode argument parsing and error handling."""

import pytest
import sys
from io import StringIO
from unittest.mock import patch
from src.cli import parse_args, execute_cli, cli_main
from src.validation import OperandValidationError


class TestParseArgsValidation:
    """Test suite for parse_args() function."""

    def test_parse_args_valid_single_operand(self):
        """Test parsing valid operation with single operand."""
        operation, operands = parse_args(["factorial", "5"])
        assert operation == "factorial"
        assert operands == [5.0]

    def test_parse_args_valid_two_operands(self):
        """Test parsing valid operation with two operands."""
        operation, operands = parse_args(["add", "3", "5"])
        assert operation == "add"
        assert operands == [3.0, 5.0]

    @pytest.mark.parametrize(
        "argv,expected_op,expected_operands",
        [
            (["add", "1", "2"], "add", [1.0, 2.0]),
            (["subtract", "10", "3"], "subtract", [10.0, 3.0]),
            (["multiply", "-5", "3"], "multiply", [-5.0, 3.0]),
            (["divide", "10.5", "2.5"], "divide", [10.5, 2.5]),
            (["square", "4"], "square", [4.0]),
            (["square_root", "16"], "square_root", [16.0]),
            (["power", "2", "10"], "power", [2.0, 10.0]),
            (["factorial", "0"], "factorial", [0.0]),
        ],
    )
    def test_parse_args_valid_operations(self, argv, expected_op, expected_operands):
        """Test parsing various valid operations with different operands."""
        operation, operands = parse_args(argv)
        assert operation == expected_op
        assert operands == expected_operands

    @pytest.mark.parametrize(
        "invalid_operand",
        [
            "abc",
            "xyz",
            "12.34.56",
            "!@#$",
        ],
    )
    def test_parse_args_invalid_operand_raises_error(self, invalid_operand):
        """Test that invalid operands raise OperandValidationError."""
        with pytest.raises(OperandValidationError):
            parse_args(["add", "5", invalid_operand])

    def test_parse_args_empty_argv_exits(self, capsys):
        """Test that empty argv prints usage and exits."""
        with pytest.raises(SystemExit) as exc_info:
            parse_args([])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Usage:" in captured.err

    def test_parse_args_negative_numbers(self):
        """Test that negative numbers are parsed correctly."""
        operation, operands = parse_args(["add", "-5", "-3"])
        assert operands == [-5.0, -3.0]

    def test_parse_args_scientific_notation(self):
        """Test parsing scientific notation operands."""
        operation, operands = parse_args(["multiply", "1e5", "2e-3"])
        assert operands == [1e5, 2e-3]

    def test_parse_args_zero(self):
        """Test that zero is parsed correctly."""
        operation, operands = parse_args(["add", "0", "5"])
        assert operands == [0.0, 5.0]

    def test_parse_args_error_message_includes_context(self):
        """Test that error message indicates which operand failed."""
        with pytest.raises(OperandValidationError) as exc_info:
            parse_args(["add", "5", "invalid"])
        assert "invalid" in str(exc_info.value).lower()

    def test_parse_args_multiple_operands_first_invalid(self):
        """Test that first invalid operand is caught."""
        with pytest.raises(OperandValidationError):
            parse_args(["add", "invalid", "5"])

    def test_parse_args_multiple_operands_second_invalid(self):
        """Test that second invalid operand is caught."""
        with pytest.raises(OperandValidationError):
            parse_args(["add", "5", "invalid"])

    def test_parse_args_many_operands(self):
        """Test parsing with many operands."""
        # While calculator may not support many operands,
        # parse_args should handle them without error
        operation, operands = parse_args(["op", "1", "2", "3", "4", "5"])
        assert operation == "op"
        assert operands == [1.0, 2.0, 3.0, 4.0, 5.0]

    def test_parse_args_whitespace_in_operands(self):
        """Test that operands are not pre-stripped (input() strips them)."""
        # parse_args receives already-split argv, so no extra whitespace
        operation, operands = parse_args(["add", "5", "3"])
        assert operands == [5.0, 3.0]


class TestExecuteCliValidation:
    """Test suite for execute_cli() function."""

    def test_execute_cli_valid_operation(self):
        """Test executing a valid operation."""
        result = execute_cli("add", [3.0, 5.0])
        assert result == 8.0

    @pytest.mark.parametrize(
        "operation,operands,expected",
        [
            ("add", [1.0, 2.0], 3.0),
            ("subtract", [10.0, 3.0], 7.0),
            ("multiply", [4.0, 5.0], 20.0),
            ("divide", [10.0, 2.0], 5.0),
            ("square", [5.0], 25.0),
            ("cube", [3.0], 27.0),
            ("factorial", [5.0], 120),
        ],
    )
    def test_execute_cli_various_operations(self, operation, operands, expected):
        """Test executing various operations."""
        result = execute_cli(operation, operands)
        assert result == expected

    def test_execute_cli_invalid_operation_raises_keyerror(self):
        """Test that invalid operation raises KeyError."""
        with pytest.raises(KeyError):
            execute_cli("unknown_operation", [1.0, 2.0])

    def test_execute_cli_wrong_operand_count_raises_error(self):
        """Test that wrong number of operands raises ValueError."""
        with pytest.raises(ValueError):
            execute_cli("add", [1.0])  # add needs 2 operands

    def test_execute_cli_too_many_operands_raises_error(self):
        """Test that too many operands raises ValueError."""
        with pytest.raises(ValueError):
            execute_cli("add", [1.0, 2.0, 3.0])  # add only takes 2

    def test_execute_cli_factorial_converts_to_int(self):
        """Test that factorial operation converts float to int."""
        # factorial should convert 5.0 to 5
        result = execute_cli("factorial", [5.0])
        assert result == 120

    def test_execute_cli_factorial_truncates_float(self):
        """Test that factorial truncates floats (e.g., 5.9 -> 5)."""
        result = execute_cli("factorial", [5.9])
        assert result == 120  # int(5.9) = 5, 5! = 120

    def test_execute_cli_division_by_zero_raises_error(self):
        """Test that division by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            execute_cli("divide", [5.0, 0.0])

    def test_execute_cli_negative_factorial_raises_error(self):
        """Test that factorial of negative number raises ValueError."""
        with pytest.raises(ValueError):
            execute_cli("factorial", [-1.0])

    def test_execute_cli_square_root_negative_raises_error(self):
        """Test that square root of negative raises ValueError."""
        with pytest.raises(ValueError):
            execute_cli("square_root", [-1.0])


class TestCliMainErrorHandling:
    """Test suite for cli_main() error handling."""

    def test_cli_main_valid_operation_exits_zero(self, capsys):
        """Test that valid operation exits with code 0."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["add", "3", "5"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "8" in captured.out

    def test_cli_main_invalid_operand_exits_one_prints_stderr(self, capsys):
        """Test that invalid operand exits with code 1 and prints to stderr."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["add", "abc", "5"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err
        assert "abc" in captured.err.lower() or "invalid" in captured.err.lower()

    def test_cli_main_invalid_operation_exits_one_prints_stderr(self, capsys):
        """Test that invalid operation exits with code 1 and prints to stderr."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["unknown_op", "5", "3"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err
        assert "invalid operation" in captured.err.lower() or "unknown" in captured.err.lower()

    def test_cli_main_wrong_operand_count_exits_one(self, capsys):
        """Test that wrong operand count exits with code 1."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["add", "5"])  # add needs 2 operands
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_cli_main_division_by_zero_exits_one(self, capsys):
        """Test that division by zero exits with code 1."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["divide", "5", "0"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_cli_main_no_args_prints_usage_and_exits_one(self, capsys):
        """Test that no arguments prints usage and exits with code 1."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main([])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Usage:" in captured.err

    @pytest.mark.parametrize(
        "args,expected_output",
        [
            (["add", "2", "3"], "5"),
            (["subtract", "10", "3"], "7"),
            (["multiply", "4", "5"], "20"),
            (["divide", "10", "2"], "5"),
            (["square", "5"], "25"),
        ],
    )
    def test_cli_main_valid_operations_output(self, args, expected_output, capsys):
        """Test that valid operations produce correct output."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(args)
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert expected_output in captured.out

    def test_cli_main_float_result_formatting(self, capsys):
        """Test that float results are formatted correctly."""
        # 5 / 2 = 2.5, should not show as "2.5"
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["divide", "5", "2"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "2.5" in captured.out

    def test_cli_main_integer_result_no_decimal(self, capsys):
        """Test that integer results are formatted without .0."""
        # 5 + 3 = 8.0, but should print as "8"
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["add", "5", "3"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        # Should be "8" not "8.0"
        assert "8" in captured.out
        assert "8.0" not in captured.out

    def test_cli_main_factorial_formats_result(self, capsys):
        """Test that factorial result is formatted as integer."""
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["factorial", "5"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "120" in captured.out
