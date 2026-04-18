"""Comprehensive pytest tests for the CLI module.

Tests cover:
- Happy path operations (one-operand and two-operand)
- Operand validation and coercion
- Error handling (domain errors, division by zero, type errors)
- Stdout/stderr separation
- Exit codes
- Edge cases (zero, negative, large numbers, special values)
"""

import pytest
import sys
from io import StringIO
from unittest.mock import Mock

from src.calculator import Calculator
from src.cli import CliDispatcher
from src.input_handler import OPERATIONS
from src.logger import Logger


# ===========================================================================
# Fixtures
# ===========================================================================


@pytest.fixture
def calc():
    """Create a fresh Calculator instance for each test."""
    return Calculator()


@pytest.fixture
def dispatcher(calc):
    """Create a CliDispatcher with a fresh Calculator."""
    return CliDispatcher(calc)


# ===========================================================================
# Test: dispatch_from_args - Happy Path (Two-Operand Operations)
# ===========================================================================


def test_dispatch_from_args_add_happy_path(dispatcher, capsys):
    """Test add operation with valid arguments."""
    exit_code = dispatcher.dispatch_from_args(["add", "5", "7"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "12.0"
    assert captured.err == ""


def test_dispatch_from_args_subtract_happy_path(dispatcher, capsys):
    """Test subtract operation with valid arguments."""
    exit_code = dispatcher.dispatch_from_args(["subtract", "10", "3"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "7.0"
    assert captured.err == ""


def test_dispatch_from_args_multiply_happy_path(dispatcher, capsys):
    """Test multiply operation with valid arguments."""
    exit_code = dispatcher.dispatch_from_args(["multiply", "4", "6"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "24.0"
    assert captured.err == ""


def test_dispatch_from_args_divide_happy_path(dispatcher, capsys):
    """Test divide operation with valid arguments."""
    exit_code = dispatcher.dispatch_from_args(["divide", "10", "2"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "5.0"
    assert captured.err == ""


def test_dispatch_from_args_power_happy_path(dispatcher, capsys):
    """Test power operation with valid arguments."""
    exit_code = dispatcher.dispatch_from_args(["power", "2", "3"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "8.0"
    assert captured.err == ""


# ===========================================================================
# Test: dispatch_from_args - Happy Path (One-Operand Operations)
# ===========================================================================


def test_dispatch_from_args_factorial_happy_path(dispatcher, capsys):
    """Test factorial operation with valid argument."""
    exit_code = dispatcher.dispatch_from_args(["factorial", "5"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "120"
    assert captured.err == ""


def test_dispatch_from_args_square_happy_path(dispatcher, capsys):
    """Test square operation with valid argument."""
    exit_code = dispatcher.dispatch_from_args(["square", "7"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "49.0"
    assert captured.err == ""


def test_dispatch_from_args_cube_happy_path(dispatcher, capsys):
    """Test cube operation with valid argument."""
    exit_code = dispatcher.dispatch_from_args(["cube", "3"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "27.0"
    assert captured.err == ""


def test_dispatch_from_args_square_root_happy_path(dispatcher, capsys):
    """Test square_root operation with valid argument."""
    exit_code = dispatcher.dispatch_from_args(["square_root", "16"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "4.0"
    assert captured.err == ""


def test_dispatch_from_args_cube_root_happy_path(dispatcher, capsys):
    """Test cube_root operation with valid argument."""
    exit_code = dispatcher.dispatch_from_args(["cube_root", "8"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "2.0"
    assert captured.err == ""


def test_dispatch_from_args_log10_happy_path(dispatcher, capsys):
    """Test log10 operation with valid argument."""
    exit_code = dispatcher.dispatch_from_args(["log10", "100"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "2.0"
    assert captured.err == ""


def test_dispatch_from_args_ln_happy_path(dispatcher, capsys):
    """Test ln operation with valid argument."""
    exit_code = dispatcher.dispatch_from_args(["ln", "2.718281828"])
    assert exit_code == 0
    captured = capsys.readouterr()
    result = float(captured.out.strip())
    assert abs(result - 1.0) < 0.01  # ln(e) ≈ 1
    assert captured.err == ""


# ===========================================================================
# Test: dispatch_from_args - Case-Insensitivity
# ===========================================================================


def test_dispatch_from_args_uppercase_operation(dispatcher, capsys):
    """Test that operation names are case-insensitive (converted to lowercase)."""
    exit_code = dispatcher.dispatch_from_args(["ADD", "5", "3"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "8.0"
    assert captured.err == ""


def test_dispatch_from_args_mixed_case_operation(dispatcher, capsys):
    """Test mixed-case operation names."""
    exit_code = dispatcher.dispatch_from_args(["FaCtOrIaL", "4"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "24"
    assert captured.err == ""


# ===========================================================================
# Test: dispatch_from_args - Empty Arguments
# ===========================================================================


def test_dispatch_from_args_empty_args(dispatcher, capsys):
    """Test with no arguments; should print usage and return error code 1."""
    exit_code = dispatcher.dispatch_from_args([])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Usage: python main.py <operation> <operand1> [<operand2>]" in captured.err
    assert "Available operations:" in captured.err


# ===========================================================================
# Test: dispatch_from_args - Unknown Operation
# ===========================================================================


def test_dispatch_from_args_unknown_operation(dispatcher, capsys):
    """Test with an operation that does not exist."""
    exit_code = dispatcher.dispatch_from_args(["unknown_op", "5"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Unknown operation 'unknown_op'" in captured.err
    assert "Available operations:" in captured.err


def test_dispatch_from_args_typo_in_operation(dispatcher, capsys):
    """Test with a slightly misspelled operation name."""
    exit_code = dispatcher.dispatch_from_args(["addx", "5", "3"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Unknown operation 'addx'" in captured.err


# ===========================================================================
# Test: dispatch_from_args - Wrong Operand Count
# ===========================================================================


def test_dispatch_from_args_too_few_operands_two_operand_op(dispatcher, capsys):
    """Test two-operand operation with too few arguments."""
    exit_code = dispatcher.dispatch_from_args(["add", "5"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "requires 2 operand(s)" in captured.err
    assert "but 1 were given" in captured.err


def test_dispatch_from_args_too_many_operands_two_operand_op(dispatcher, capsys):
    """Test two-operand operation with too many arguments."""
    exit_code = dispatcher.dispatch_from_args(["add", "5", "3", "2"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "requires 2 operand(s)" in captured.err
    assert "but 3 were given" in captured.err


def test_dispatch_from_args_too_many_operands_one_operand_op(dispatcher, capsys):
    """Test one-operand operation with too many arguments."""
    exit_code = dispatcher.dispatch_from_args(["factorial", "5", "3"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "requires 1 operand(s)" in captured.err
    assert "but 2 were given" in captured.err


def test_dispatch_from_args_no_operands_for_one_operand_op(dispatcher, capsys):
    """Test one-operand operation with no arguments."""
    exit_code = dispatcher.dispatch_from_args(["square"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "requires 1 operand(s)" in captured.err


# ===========================================================================
# Test: dispatch_from_args - Invalid Operand Coercion
# ===========================================================================


def test_dispatch_from_args_invalid_operand_not_numeric(dispatcher, capsys):
    """Test with a non-numeric operand string."""
    exit_code = dispatcher.dispatch_from_args(["add", "abc", "5"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Invalid operand 'abc'" in captured.err
    assert "expected a numeric value" in captured.err


def test_dispatch_from_args_invalid_operand_second_operand(dispatcher, capsys):
    """Test with invalid second operand."""
    exit_code = dispatcher.dispatch_from_args(["add", "5", "xyz"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Invalid operand 'xyz'" in captured.err


def test_dispatch_from_args_invalid_operand_special_chars(dispatcher, capsys):
    """Test with special characters that are not numeric."""
    exit_code = dispatcher.dispatch_from_args(["add", "5@3", "2"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Invalid operand '5@3'" in captured.err


def test_dispatch_from_args_invalid_operand_empty_string(dispatcher, capsys):
    """Test with empty string as operand."""
    exit_code = dispatcher.dispatch_from_args(["add", "", "5"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Invalid operand ''" in captured.err


# ===========================================================================
# Test: dispatch_from_args - Factorial Requires Integer
# ===========================================================================


def test_dispatch_from_args_factorial_with_float(dispatcher, capsys):
    """Test factorial with a float (which should fail since coerce=int)."""
    exit_code = dispatcher.dispatch_from_args(["factorial", "5.5"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Invalid operand '5.5'" in captured.err


def test_dispatch_from_args_factorial_zero(dispatcher, capsys):
    """Test factorial of zero; should return 1."""
    exit_code = dispatcher.dispatch_from_args(["factorial", "0"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "1"


def test_dispatch_from_args_factorial_one(dispatcher, capsys):
    """Test factorial of one; should return 1."""
    exit_code = dispatcher.dispatch_from_args(["factorial", "1"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "1"


def test_dispatch_from_args_factorial_large_number(dispatcher, capsys):
    """Test factorial of a larger number."""
    exit_code = dispatcher.dispatch_from_args(["factorial", "10"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "3628800"


# ===========================================================================
# Test: dispatch_from_args - Division by Zero
# ===========================================================================


def test_dispatch_from_args_divide_by_zero(dispatcher, capsys):
    """Test division by zero; should catch ZeroDivisionError."""
    exit_code = dispatcher.dispatch_from_args(["divide", "10", "0"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Division by zero is not allowed" in captured.err


def test_dispatch_from_args_power_zero_exponent(dispatcher, capsys):
    """Test power with zero exponent; should return 1."""
    exit_code = dispatcher.dispatch_from_args(["power", "5", "0"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "1.0"


# ===========================================================================
# Test: dispatch_from_args - Domain Errors (sqrt, log)
# ===========================================================================


def test_dispatch_from_args_square_root_negative(dispatcher, capsys):
    """Test square_root with negative number; should raise ValueError."""
    exit_code = dispatcher.dispatch_from_args(["square_root", "-4"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "not defined for negative" in captured.err.lower()


def test_dispatch_from_args_log10_zero(dispatcher, capsys):
    """Test log10 of zero; should raise ValueError."""
    exit_code = dispatcher.dispatch_from_args(["log10", "0"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "not defined for x <= 0" in captured.err


def test_dispatch_from_args_log10_negative(dispatcher, capsys):
    """Test log10 of negative number; should raise ValueError."""
    exit_code = dispatcher.dispatch_from_args(["log10", "-10"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "not defined for x <= 0" in captured.err


def test_dispatch_from_args_ln_zero(dispatcher, capsys):
    """Test ln of zero; should raise ValueError."""
    exit_code = dispatcher.dispatch_from_args(["ln", "0"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "not defined for x <= 0" in captured.err


def test_dispatch_from_args_ln_negative(dispatcher, capsys):
    """Test ln of negative number; should raise ValueError."""
    exit_code = dispatcher.dispatch_from_args(["ln", "-5"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "not defined for x <= 0" in captured.err


# ===========================================================================
# Test: dispatch_from_args - Factorial Type Errors
# ===========================================================================


def test_dispatch_from_args_factorial_negative(dispatcher, capsys):
    """Test factorial with negative integer; should raise ValueError."""
    exit_code = dispatcher.dispatch_from_args(["factorial", "-5"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "negative" in captured.err.lower()


# ===========================================================================
# Test: _coerce_operands - Happy Path
# ===========================================================================


def test_coerce_operands_floats(dispatcher):
    """Test coercing strings to floats."""
    result = dispatcher._coerce_operands(["3.14", "2.71"], float)
    assert result == [3.14, 2.71]


def test_coerce_operands_integers(dispatcher):
    """Test coercing strings to integers."""
    result = dispatcher._coerce_operands(["5", "10"], int)
    assert result == [5, 10]


def test_coerce_operands_single_operand(dispatcher):
    """Test coercing a single operand."""
    result = dispatcher._coerce_operands(["7"], float)
    assert result == [7.0]


def test_coerce_operands_negative_numbers(dispatcher):
    """Test coercing negative numbers."""
    result = dispatcher._coerce_operands(["-5", "-10.5"], float)
    assert result == [-5.0, -10.5]


def test_coerce_operands_zero(dispatcher):
    """Test coercing zero."""
    result = dispatcher._coerce_operands(["0", "0.0"], float)
    assert result == [0.0, 0.0]


def test_coerce_operands_scientific_notation(dispatcher):
    """Test coercing scientific notation."""
    result = dispatcher._coerce_operands(["1e5", "2.5e-2"], float)
    assert result == [100000.0, 0.025]


# ===========================================================================
# Test: _coerce_operands - Error Cases
# ===========================================================================


def test_coerce_operands_invalid_float(dispatcher):
    """Test that invalid float string raises ValueError."""
    with pytest.raises(ValueError, match="Invalid operand"):
        dispatcher._coerce_operands(["abc"], float)


def test_coerce_operands_invalid_integer(dispatcher):
    """Test that float string raises ValueError when int coerce expected."""
    with pytest.raises(ValueError, match="Invalid operand"):
        dispatcher._coerce_operands(["3.14"], int)


def test_coerce_operands_first_operand_invalid(dispatcher):
    """Test that invalid first operand is caught."""
    with pytest.raises(ValueError, match="Invalid operand 'xyz'"):
        dispatcher._coerce_operands(["xyz", "5"], float)


def test_coerce_operands_second_operand_invalid(dispatcher):
    """Test that invalid second operand is caught."""
    with pytest.raises(ValueError, match="Invalid operand 'abc'"):
        dispatcher._coerce_operands(["5", "abc"], float)


def test_coerce_operands_empty_list(dispatcher):
    """Test coercing an empty list returns empty list."""
    result = dispatcher._coerce_operands([], float)
    assert result == []


def test_coerce_operands_whitespace_only_string(dispatcher):
    """Test that whitespace-only string raises ValueError."""
    with pytest.raises(ValueError, match="Invalid operand"):
        dispatcher._coerce_operands(["   "], float)


# ===========================================================================
# Test: _dispatch - Happy Path
# ===========================================================================


def test_dispatch_add(dispatcher):
    """Test dispatching to add method."""
    result = dispatcher._dispatch("add", [5, 7])
    assert result == 12


def test_dispatch_subtract(dispatcher):
    """Test dispatching to subtract method."""
    result = dispatcher._dispatch("subtract", [10, 3])
    assert result == 7


def test_dispatch_multiply(dispatcher):
    """Test dispatching to multiply method."""
    result = dispatcher._dispatch("multiply", [4, 5])
    assert result == 20


def test_dispatch_divide(dispatcher):
    """Test dispatching to divide method."""
    result = dispatcher._dispatch("divide", [10, 2])
    assert result == 5.0


def test_dispatch_factorial(dispatcher):
    """Test dispatching to factorial method."""
    result = dispatcher._dispatch("factorial", [5])
    assert result == 120


def test_dispatch_square(dispatcher):
    """Test dispatching to square method."""
    result = dispatcher._dispatch("square", [6])
    assert result == 36


def test_dispatch_cube(dispatcher):
    """Test dispatching to cube method."""
    result = dispatcher._dispatch("cube", [3])
    assert result == 27


def test_dispatch_power(dispatcher):
    """Test dispatching to power method."""
    result = dispatcher._dispatch("power", [2, 8])
    assert result == 256


# ===========================================================================
# Test: _dispatch - Error Propagation
# ===========================================================================


def test_dispatch_division_by_zero(dispatcher):
    """Test that ZeroDivisionError is propagated from divide."""
    with pytest.raises(ZeroDivisionError):
        dispatcher._dispatch("divide", [10, 0])


def test_dispatch_sqrt_negative_raises_value_error(dispatcher):
    """Test that ValueError from square_root is propagated."""
    with pytest.raises(ValueError):
        dispatcher._dispatch("square_root", [-4])


def test_dispatch_log10_zero_raises_value_error(dispatcher):
    """Test that ValueError from log10 is propagated."""
    with pytest.raises(ValueError):
        dispatcher._dispatch("log10", [0])


def test_dispatch_factorial_negative_raises_value_error(dispatcher):
    """Test that ValueError from factorial with negative is propagated."""
    with pytest.raises(ValueError):
        dispatcher._dispatch("factorial", [-5])


def test_dispatch_factorial_float_raises_type_error(dispatcher):
    """Test that TypeError from factorial with float is propagated."""
    with pytest.raises(TypeError):
        dispatcher._dispatch("factorial", [5.5])


# ===========================================================================
# Test: _print_error - Output Format
# ===========================================================================


def test_print_error_format(capsys):
    """Test that _print_error writes to stderr with 'Error: ' prefix."""
    CliDispatcher._print_error("This is an error message")
    captured = capsys.readouterr()
    assert captured.err == "Error: This is an error message\n"
    assert captured.out == ""


def test_print_error_empty_message(capsys):
    """Test _print_error with empty message."""
    CliDispatcher._print_error("")
    captured = capsys.readouterr()
    assert captured.err == "Error: \n"


def test_print_error_multiline_message(capsys):
    """Test _print_error with newlines in message."""
    CliDispatcher._print_error("Line 1\nLine 2")
    captured = capsys.readouterr()
    assert "Error: Line 1\nLine 2\n" == captured.err


def test_print_error_special_chars(capsys):
    """Test _print_error with special characters."""
    CliDispatcher._print_error("Error with special chars: @#$%")
    captured = capsys.readouterr()
    assert "Error: Error with special chars: @#$%\n" == captured.err


# ===========================================================================
# Test: Stdout/Stderr Separation - Comprehensive
# ===========================================================================


def test_success_goes_to_stdout_not_stderr(dispatcher, capsys):
    """Test that successful result goes to stdout, not stderr."""
    exit_code = dispatcher.dispatch_from_args(["add", "3", "4"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "7.0"
    assert captured.err == ""


def test_error_goes_to_stderr_not_stdout(dispatcher, capsys):
    """Test that error message goes to stderr, not stdout."""
    exit_code = dispatcher.dispatch_from_args(["unknown_op", "5"])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert "Error:" in captured.err


def test_validation_error_goes_to_stderr(dispatcher, capsys):
    """Test that validation errors go to stderr."""
    exit_code = dispatcher.dispatch_from_args(["add", "abc"])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert "Error:" in captured.err


# ===========================================================================
# Test: Edge Cases - Numeric Boundaries
# ===========================================================================


def test_dispatch_large_numbers_add(dispatcher, capsys):
    """Test add with very large numbers."""
    exit_code = dispatcher.dispatch_from_args(["add", "1e20", "2e20"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert float(captured.out.strip()) == 3e20


def test_dispatch_very_small_numbers_add(dispatcher, capsys):
    """Test add with very small numbers."""
    exit_code = dispatcher.dispatch_from_args(["add", "1e-20", "2e-20"])
    assert exit_code == 0
    captured = capsys.readouterr()
    result = float(captured.out.strip())
    assert abs(result - 3e-20) < 1e-21


def test_dispatch_negative_multiply(dispatcher, capsys):
    """Test multiply with negative numbers."""
    exit_code = dispatcher.dispatch_from_args(["multiply", "-5", "4"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "-20.0"


def test_dispatch_negative_divide(dispatcher, capsys):
    """Test divide with negative numbers."""
    exit_code = dispatcher.dispatch_from_args(["divide", "-10", "2"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "-5.0"


def test_dispatch_square_negative(dispatcher, capsys):
    """Test square with negative number."""
    exit_code = dispatcher.dispatch_from_args(["square", "-5"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "25.0"


def test_dispatch_cube_negative(dispatcher, capsys):
    """Test cube with negative number."""
    exit_code = dispatcher.dispatch_from_args(["cube", "-2"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "-8.0"


def test_dispatch_cube_root_negative(dispatcher, capsys):
    """Test cube_root with negative number (should work for cube root)."""
    exit_code = dispatcher.dispatch_from_args(["cube_root", "-8"])
    assert exit_code == 0
    captured = capsys.readouterr()
    result = float(captured.out.strip())
    assert abs(result - (-2.0)) < 0.01


# ===========================================================================
# Test: Parametrized Tests for All Operations
# ===========================================================================


@pytest.mark.parametrize("op_key,operands,expected", [
    ("add", ["2", "3"], "5.0"),
    ("subtract", ["10", "4"], "6.0"),
    ("multiply", ["3", "7"], "21.0"),
    ("divide", ["20", "4"], "5.0"),
    ("power", ["3", "2"], "9.0"),
])
def test_two_operand_operations(dispatcher, capsys, op_key, operands, expected):
    """Test all two-operand operations with parametrized data."""
    exit_code = dispatcher.dispatch_from_args([op_key] + operands)
    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == expected


@pytest.mark.parametrize("op_key,operand,expected", [
    ("factorial", "3", "6"),
    ("square", "5", "25.0"),
    ("cube", "2", "8.0"),
    ("square_root", "9", "3.0"),
    ("log10", "10", "1.0"),
])
def test_one_operand_operations(dispatcher, capsys, op_key, operand, expected):
    """Test all one-operand operations with parametrized data."""
    exit_code = dispatcher.dispatch_from_args([op_key, operand])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == expected


def test_one_operand_operations_cube_root(dispatcher, capsys):
    """Test cube_root with approximate comparison due to floating point precision."""
    exit_code = dispatcher.dispatch_from_args(["cube_root", "27"])
    assert exit_code == 0
    captured = capsys.readouterr()
    result = float(captured.out.strip())
    assert abs(result - 3.0) < 1e-10


# ===========================================================================
# Test: All Operations Available in Registry
# ===========================================================================


def test_all_registered_operations_can_be_dispatched(dispatcher, calc):
    """Test that every operation in the registry can be dispatched."""
    for op_key, op_info in OPERATIONS.items():
        arity = op_info["arity"]
        coerce = op_info.get("coerce", float)

        # Create dummy operands with correct count
        if arity == 1:
            # Use a valid operand for each operation
            if op_key == "factorial":
                operands = [5]
            elif op_key in ("square_root", "ln", "log10"):
                operands = [10]  # positive values for these
            else:
                operands = [5]
        else:  # arity == 2
            operands = [5, 3]

        # Should not raise
        result = dispatcher._dispatch(op_key, operands)
        assert result is not None


# ===========================================================================
# Test: Integration - main() entry point behavior
# ===========================================================================


def test_cli_importer_exports_cli_dispatcher():
    """Test that CliDispatcher is importable from src module."""
    from src import CliDispatcher as ImportedDispatcher
    assert ImportedDispatcher is CliDispatcher


def test_cli_importer_exports_calculator():
    """Test that Calculator is importable from src module."""
    from src import Calculator as ImportedCalculator
    assert ImportedCalculator is Calculator


# ===========================================================================
# Test: Logger Integration
# ===========================================================================


def test_unknown_operation_is_logged(calc):
    """Unknown operation should be logged via log_unsupported_operation."""
    mock_logger = Mock(spec=Logger)
    dispatcher = CliDispatcher(calc, logger=mock_logger)
    dispatcher.dispatch_from_args(["unknown_op", "5"])

    # Verify logger was called
    mock_logger.log_unsupported_operation.assert_called()
    call_args = mock_logger.log_unsupported_operation.call_args
    assert call_args[0][0] == "unknown_op"


def test_invalid_argument_count_is_logged(calc):
    """Invalid argument count should be logged via log_invalid_argument_count."""
    mock_logger = Mock(spec=Logger)
    dispatcher = CliDispatcher(calc, logger=mock_logger)
    dispatcher.dispatch_from_args(["add", "5"])  # Missing second operand

    # Verify logger was called
    mock_logger.log_invalid_argument_count.assert_called()
    call_args = mock_logger.log_invalid_argument_count.call_args
    assert call_args[0][0] == "add"  # operation
    assert call_args[0][1] == 2  # expected
    assert call_args[0][2] == 1  # given


def test_invalid_operand_is_logged(calc):
    """Invalid operand should be logged via log_invalid_operand."""
    mock_logger = Mock(spec=Logger)
    dispatcher = CliDispatcher(calc, logger=mock_logger)
    dispatcher.dispatch_from_args(["add", "abc", "5"])

    # Verify logger was called
    mock_logger.log_invalid_operand.assert_called()
    call_args = mock_logger.log_invalid_operand.call_args
    assert call_args[0][0] == "abc"  # raw value
    assert call_args[0][1] == "<numeric>"  # expected type


def test_division_by_zero_is_logged_cli(calc):
    """Division by zero should be logged via log_division_by_zero."""
    mock_logger = Mock(spec=Logger)
    dispatcher = CliDispatcher(calc, logger=mock_logger)
    dispatcher.dispatch_from_args(["divide", "10", "0"])

    # Verify logger was called
    mock_logger.log_division_by_zero.assert_called()
    call_args = mock_logger.log_division_by_zero.call_args
    assert call_args[0][0] == [10.0, 0.0]  # operands


def test_domain_error_sqrt_negative_is_logged_cli(calc):
    """Domain error (sqrt of negative) should be logged via log_domain_error."""
    mock_logger = Mock(spec=Logger)
    dispatcher = CliDispatcher(calc, logger=mock_logger)
    dispatcher.dispatch_from_args(["square_root", "-4"])

    # Verify logger was called
    mock_logger.log_domain_error.assert_called()
    call_args = mock_logger.log_domain_error.call_args
    assert call_args[0][0] == "square_root"  # operation


def test_domain_error_log10_zero_is_logged_cli(calc):
    """Domain error (log10 of zero) should be logged via log_domain_error."""
    mock_logger = Mock(spec=Logger)
    dispatcher = CliDispatcher(calc, logger=mock_logger)
    dispatcher.dispatch_from_args(["log10", "0"])

    # Verify logger was called
    mock_logger.log_domain_error.assert_called()
    call_args = mock_logger.log_domain_error.call_args
    assert call_args[0][0] == "log10"


def test_domain_error_factorial_negative_is_logged_cli(calc):
    """Domain error (factorial of negative) should be logged via log_domain_error."""
    mock_logger = Mock(spec=Logger)
    dispatcher = CliDispatcher(calc, logger=mock_logger)
    dispatcher.dispatch_from_args(["factorial", "-5"])

    # Verify logger was called
    mock_logger.log_domain_error.assert_called()
    call_args = mock_logger.log_domain_error.call_args
    assert call_args[0][0] == "factorial"


def test_successful_operation_does_not_log_error_cli(calc):
    """Successful operations should not call any logger error methods."""
    mock_logger = Mock(spec=Logger)
    dispatcher = CliDispatcher(calc, logger=mock_logger)
    dispatcher.dispatch_from_args(["add", "3", "4"])

    # None of the error logging methods should be called
    assert not mock_logger.log_unsupported_operation.called
    assert not mock_logger.log_invalid_operand.called
    assert not mock_logger.log_division_by_zero.called
    assert not mock_logger.log_domain_error.called
    assert not mock_logger.log_invalid_argument_count.called


def test_logger_lazy_initialization_cli(calc):
    """Logger should be lazily initialized if not provided."""
    dispatcher = CliDispatcher(calc)
    assert dispatcher._logger is None  # Not initialized yet

    dispatcher.dispatch_from_args(["add", "5", "3"])
    assert dispatcher._logger is not None  # Now initialized


def test_logger_injection_prevents_lazy_creation_cli(calc):
    """Injected logger should prevent lazy creation."""
    injected_logger = Mock(spec=Logger)
    dispatcher = CliDispatcher(calc, logger=injected_logger)
    assert dispatcher._logger is injected_logger

    dispatcher.dispatch_from_args(["add", "5", "3"])
    # Should still be the injected logger
    assert dispatcher._logger is injected_logger


def test_empty_args_is_not_logged_as_error(calc):
    """Empty args should not trigger any logging (it's just usage info)."""
    mock_logger = Mock(spec=Logger)
    dispatcher = CliDispatcher(calc, logger=mock_logger)
    dispatcher.dispatch_from_args([])

    # No error logging should occur for usage info
    assert not mock_logger.log_unsupported_operation.called
    assert not mock_logger.log_invalid_argument_count.called
    assert not mock_logger.log_invalid_operand.called
    assert not mock_logger.log_division_by_zero.called
    assert not mock_logger.log_domain_error.called
