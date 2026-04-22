"""Unit tests for CLIHandler class."""

import pytest
import sys
from io import StringIO
from src.cli_handler import CLIHandler


class TestParseArguments:
    """Test suite for CLIHandler.parse_arguments() method."""

    @pytest.fixture
    def handler(self):
        """Fixture to provide a CLIHandler instance."""
        return CLIHandler()

    def test_parse_arguments_binary_operation(self, handler):
        """Test parsing arguments for a binary operation."""
        operation_key, operands = handler.parse_arguments(["add", "5", "3"])
        assert operation_key == "add"
        assert operands == ["5", "3"]

    def test_parse_arguments_unary_operation(self, handler):
        """Test parsing arguments for a unary operation."""
        operation_key, operands = handler.parse_arguments(["square", "5"])
        assert operation_key == "square"
        assert operands == ["5"]

    @pytest.mark.parametrize("args,expected_op,expected_operands", [
        (["add", "5", "3"], "add", ["5", "3"]),
        (["subtract", "10", "4"], "subtract", ["10", "4"]),
        (["multiply", "2", "6"], "multiply", ["2", "6"]),
        (["divide", "8", "2"], "divide", ["8", "2"]),
    ])
    def test_parse_arguments_various_binary_ops(self, handler, args, expected_op, expected_operands):
        """Test parsing arguments for various binary operations."""
        operation_key, operands = handler.parse_arguments(args)
        assert operation_key == expected_op
        assert operands == expected_operands

    @pytest.mark.parametrize("args,expected_op,expected_operands", [
        (["square", "5"], "square", ["5"]),
        (["square_root", "16"], "square_root", ["16"]),
        (["factorial", "5"], "factorial", ["5"]),
        (["cube", "3"], "cube", ["3"]),
    ])
    def test_parse_arguments_various_unary_ops(self, handler, args, expected_op, expected_operands):
        """Test parsing arguments for various unary operations."""
        operation_key, operands = handler.parse_arguments(args)
        assert operation_key == expected_op
        assert operands == expected_operands

    def test_parse_arguments_negative_numbers(self, handler):
        """Test parsing arguments with negative numbers."""
        operation_key, operands = handler.parse_arguments(["subtract", "-5", "-3"])
        assert operation_key == "subtract"
        assert operands == ["-5", "-3"]

    def test_parse_arguments_float_operands(self, handler):
        """Test parsing arguments with floating-point operands."""
        operation_key, operands = handler.parse_arguments(["divide", "5.5", "2.2"])
        assert operation_key == "divide"
        assert operands == ["5.5", "2.2"]

    def test_parse_arguments_scientific_notation(self, handler):
        """Test parsing arguments with scientific notation."""
        operation_key, operands = handler.parse_arguments(["multiply", "1e5", "2e3"])
        assert operation_key == "multiply"
        assert operands == ["1e5", "2e3"]

    def test_parse_arguments_empty_args_raises_valueerror(self, handler):
        """Test that empty arguments raise ValueError."""
        with pytest.raises(ValueError, match="No arguments provided"):
            handler.parse_arguments([])

    def test_parse_arguments_only_operation_no_operands(self, handler):
        """Test parsing when only operation is provided (no operands)."""
        operation_key, operands = handler.parse_arguments(["add"])
        assert operation_key == "add"
        assert operands == []

    def test_parse_arguments_many_operands(self, handler):
        """Test parsing when more than 2 operands are provided (validation happens later)."""
        operation_key, operands = handler.parse_arguments(["add", "1", "2", "3", "4"])
        assert operation_key == "add"
        assert operands == ["1", "2", "3", "4"]


class TestValidateOperands:
    """Test suite for CLIHandler.validate_operands() method."""

    @pytest.fixture
    def handler(self):
        """Fixture to provide a CLIHandler instance."""
        return CLIHandler()

    def test_validate_operands_valid_floats(self, handler):
        """Test validation of valid float operands."""
        result = handler.validate_operands(["5.5", "2.2"], 2)
        assert result == [5.5, 2.2]
        assert all(isinstance(x, float) for x in result)

    def test_validate_operands_valid_integers(self, handler):
        """Test validation of integer strings converted to floats."""
        result = handler.validate_operands(["5", "3"], 2)
        assert result == [5.0, 3.0]
        assert all(isinstance(x, float) for x in result)

    def test_validate_operands_negative_numbers(self, handler):
        """Test validation of negative operands."""
        result = handler.validate_operands(["-5", "-3"], 2)
        assert result == [-5.0, -3.0]

    def test_validate_operands_scientific_notation(self, handler):
        """Test validation of scientific notation operands."""
        result = handler.validate_operands(["1e5", "2e3"], 2)
        assert result == [1e5, 2e3]

    @pytest.mark.parametrize("operands,arity,expected", [
        (["5"], 1, [5.0]),
        (["5", "3"], 2, [5.0, 3.0]),
        (["-5", "-3"], 2, [-5.0, -3.0]),
        (["0"], 1, [0.0]),
        (["0", "0"], 2, [0.0, 0.0]),
        (["1.5", "2.5"], 2, [1.5, 2.5]),
    ])
    def test_validate_operands_various_valid_inputs(self, handler, operands, arity, expected):
        """Test validation with various valid inputs."""
        result = handler.validate_operands(operands, arity)
        assert result == expected

    def test_validate_operands_arity_mismatch_too_few(self, handler):
        """Test that fewer operands than arity raises ValueError."""
        with pytest.raises(ValueError, match="Expected 2 operand"):
            handler.validate_operands(["5"], 2)

    def test_validate_operands_arity_mismatch_too_many(self, handler):
        """Test that more operands than arity raises ValueError."""
        with pytest.raises(ValueError, match="Expected 2 operand"):
            handler.validate_operands(["5", "3", "2"], 2)

    def test_validate_operands_arity_mismatch_empty_for_arity_one(self, handler):
        """Test that empty operands for arity 1 raises ValueError."""
        with pytest.raises(ValueError, match="Expected 1 operand"):
            handler.validate_operands([], 1)

    def test_validate_operands_non_numeric_input(self, handler):
        """Test that non-numeric input raises ValueError."""
        with pytest.raises(ValueError, match="Invalid operand 'abc': must be a numeric value"):
            handler.validate_operands(["abc", "3"], 2)

    def test_validate_operands_partially_non_numeric(self, handler):
        """Test that partially non-numeric input raises ValueError."""
        with pytest.raises(ValueError, match="Invalid operand 'xyz': must be a numeric value"):
            handler.validate_operands(["5", "xyz"], 2)

    @pytest.mark.parametrize("invalid_operand", [
        "abc",
        "12.34.56",
        "1e2e3",
        "not_a_number",
        "5 3",
    ])
    def test_validate_operands_various_invalid_inputs(self, handler, invalid_operand):
        """Test validation with various invalid inputs."""
        with pytest.raises(ValueError, match="Invalid operand"):
            handler.validate_operands([invalid_operand, "3"], 2)


class TestPrintResult:
    """Test suite for CLIHandler.print_result() method."""

    @pytest.fixture
    def handler(self):
        """Fixture to provide a CLIHandler instance."""
        return CLIHandler()

    def test_print_result_stdout_format(self, handler, capsys):
        """Test that result is printed to stdout in correct format."""
        handler.print_result("Addition", [5.0, 3.0], 8.0)
        captured = capsys.readouterr()
        assert captured.out == "Result: 8.0\n"

    def test_print_result_integer_result(self, handler, capsys):
        """Test result output with integer result."""
        handler.print_result("Multiplication", [5.0, 3.0], 15)
        captured = capsys.readouterr()
        assert captured.out == "Result: 15\n"

    def test_print_result_float_result(self, handler, capsys):
        """Test result output with float result."""
        handler.print_result("Division", [5.0, 2.0], 2.5)
        captured = capsys.readouterr()
        assert captured.out == "Result: 2.5\n"

    def test_print_result_negative_result(self, handler, capsys):
        """Test result output with negative result."""
        handler.print_result("Subtraction", [3.0, 5.0], -2.0)
        captured = capsys.readouterr()
        assert captured.out == "Result: -2.0\n"

    def test_print_result_zero_result(self, handler, capsys):
        """Test result output with zero result."""
        handler.print_result("Subtraction", [5.0, 5.0], 0.0)
        captured = capsys.readouterr()
        assert captured.out == "Result: 0.0\n"

    @pytest.mark.parametrize("description,operands,result", [
        ("Addition", [1.0, 2.0], 3.0),
        ("Subtraction", [5.0, 3.0], 2.0),
        ("Multiplication", [4.0, 5.0], 20.0),
        ("Division", [10.0, 2.0], 5.0),
        ("Square", [3.0], 9.0),
        ("Factorial", [5.0], 120.0),
    ])
    def test_print_result_various_operations(self, handler, capsys, description, operands, result):
        """Test result output for various operations."""
        handler.print_result(description, operands, result)
        captured = capsys.readouterr()
        assert captured.out == f"Result: {result}\n"

    def test_print_result_no_stderr_output(self, handler, capsys):
        """Test that result printing does not output to stderr."""
        handler.print_result("Addition", [5.0, 3.0], 8.0)
        captured = capsys.readouterr()
        assert captured.err == ""


class TestPrintError:
    """Test suite for CLIHandler.print_error() method."""

    @pytest.fixture
    def handler(self):
        """Fixture to provide a CLIHandler instance."""
        return CLIHandler()

    def test_print_error_stderr_output(self, handler, capsys):
        """Test that error is printed to stderr."""
        handler.print_error("Something went wrong")
        captured = capsys.readouterr()
        assert captured.err == "Error: Something went wrong\n"

    def test_print_error_simple_message(self, handler, capsys):
        """Test error output with simple message."""
        handler.print_error("Division by zero is not allowed.")
        captured = capsys.readouterr()
        assert "Error: Division by zero is not allowed." in captured.err

    def test_print_error_unknown_operation(self, handler, capsys):
        """Test error output for unknown operation."""
        handler.print_error("Unknown operation: 'xyz'")
        captured = capsys.readouterr()
        assert "Error: Unknown operation: 'xyz'" in captured.err

    def test_print_error_invalid_operand(self, handler, capsys):
        """Test error output for invalid operand."""
        handler.print_error("Invalid operand 'abc': must be a numeric value")
        captured = capsys.readouterr()
        assert "Error: Invalid operand 'abc': must be a numeric value" in captured.err

    def test_print_error_no_stdout_output(self, handler, capsys):
        """Test that error printing does not output to stdout."""
        handler.print_error("Something went wrong")
        captured = capsys.readouterr()
        assert captured.out == ""

    @pytest.mark.parametrize("message", [
        "Division by zero is not allowed.",
        "Expected 2 operand(s), got 1.",
        "Invalid operand 'abc': must be a numeric value.",
        "Unknown operation: 'unknown'",
        "No arguments provided. Usage: calculator <operation> [operands...]",
    ])
    def test_print_error_various_messages(self, handler, capsys, message):
        """Test error output with various messages."""
        handler.print_error(message)
        captured = capsys.readouterr()
        assert f"Error: {message}" in captured.err


class TestIsCliMode:
    """Test suite for CLIHandler.is_cli_mode() method."""

    @pytest.fixture
    def handler(self):
        """Fixture to provide a CLIHandler instance."""
        return CLIHandler()

    def test_is_cli_mode_empty_args_returns_false(self, handler):
        """Test that empty args return False."""
        assert handler.is_cli_mode([]) is False

    def test_is_cli_mode_single_arg_returns_true(self, handler):
        """Test that single arg returns True."""
        assert handler.is_cli_mode(["add"]) is True

    def test_is_cli_mode_multiple_args_returns_true(self, handler):
        """Test that multiple args return True."""
        assert handler.is_cli_mode(["add", "5", "3"]) is True

    @pytest.mark.parametrize("args", [
        ["add"],
        ["add", "5"],
        ["add", "5", "3"],
        ["square", "4"],
        ["factorial", "5"],
    ])
    def test_is_cli_mode_non_empty_returns_true(self, handler, args):
        """Test that non-empty args always return True."""
        assert handler.is_cli_mode(args) is True

    def test_is_cli_mode_return_type(self, handler):
        """Test that return value is boolean type."""
        result = handler.is_cli_mode([])
        assert isinstance(result, bool)
        result = handler.is_cli_mode(["add"])
        assert isinstance(result, bool)
