"""Comprehensive pytest tests for src/dispatcher.py.

Tests cover:
- OperationDispatcher initialization
- coerce_operands: happy path (float, int), ValueError on bad input, multi-element list
- dispatch: all 12 operations, exception propagation (ValueError, ZeroDivisionError, TypeError)
"""

import pytest
import math
from unittest.mock import Mock, MagicMock

from src.calculator import Calculator
from src.dispatcher import OperationDispatcher


# ===========================================================================
# Fixtures
# ===========================================================================


@pytest.fixture
def calc():
    """Create a fresh Calculator instance for each test."""
    return Calculator()


@pytest.fixture
def dispatcher(calc):
    """Create an OperationDispatcher with a fresh Calculator."""
    return OperationDispatcher(calc)


# ===========================================================================
# OperationDispatcher.__init__
# ===========================================================================


def test_init_stores_calculator(calc):
    """__init__ stores the provided Calculator instance."""
    dispatcher = OperationDispatcher(calc)
    assert dispatcher._calculator is calc


def test_init_with_mock_calculator():
    """__init__ accepts any object (does not enforce Calculator type at init)."""
    mock_calc = Mock()
    dispatcher = OperationDispatcher(mock_calc)
    assert dispatcher._calculator is mock_calc


# ===========================================================================
# coerce_operands: Happy Path
# ===========================================================================


def test_coerce_operands_single_float_string(dispatcher):
    """coerce_operands converts a single string to float."""
    result = dispatcher.coerce_operands(["3.14"], float)
    assert result == [3.14]
    assert isinstance(result[0], float)


def test_coerce_operands_single_int_string(dispatcher):
    """coerce_operands converts a single string to int."""
    result = dispatcher.coerce_operands(["42"], int)
    assert result == [42]
    assert isinstance(result[0], int)


def test_coerce_operands_single_int_to_float(dispatcher):
    """coerce_operands converts integer string to float."""
    result = dispatcher.coerce_operands(["5"], float)
    assert result == [5.0]
    assert isinstance(result[0], float)


def test_coerce_operands_two_floats(dispatcher):
    """coerce_operands converts multiple float strings in order."""
    result = dispatcher.coerce_operands(["2.5", "3.7"], float)
    assert result == [2.5, 3.7]
    assert len(result) == 2
    assert all(isinstance(x, float) for x in result)


def test_coerce_operands_two_ints(dispatcher):
    """coerce_operands converts multiple int strings."""
    result = dispatcher.coerce_operands(["10", "20"], int)
    assert result == [10, 20]
    assert all(isinstance(x, int) for x in result)


def test_coerce_operands_negative_float(dispatcher):
    """coerce_operands handles negative float strings."""
    result = dispatcher.coerce_operands(["-3.14"], float)
    assert result == [-3.14]


def test_coerce_operands_negative_int(dispatcher):
    """coerce_operands handles negative int strings."""
    result = dispatcher.coerce_operands(["-42"], int)
    assert result == [-42]


def test_coerce_operands_zero_float(dispatcher):
    """coerce_operands converts '0.0' to float zero."""
    result = dispatcher.coerce_operands(["0.0"], float)
    assert result == [0.0]


def test_coerce_operands_zero_int(dispatcher):
    """coerce_operands converts '0' to int zero."""
    result = dispatcher.coerce_operands(["0"], int)
    assert result == [0]


def test_coerce_operands_scientific_notation(dispatcher):
    """coerce_operands handles scientific notation strings."""
    result = dispatcher.coerce_operands(["1e10"], float)
    assert result == [1e10]


def test_coerce_operands_large_int(dispatcher):
    """coerce_operands handles very large int strings."""
    result = dispatcher.coerce_operands(["999999999999999999"], int)
    assert result == [999999999999999999]


def test_coerce_operands_large_float(dispatcher):
    """coerce_operands handles very large float strings."""
    result = dispatcher.coerce_operands(["1.79e308"], float)
    assert result == [1.79e308]


def test_coerce_operands_leading_whitespace(dispatcher):
    """coerce_operands handles strings with leading whitespace."""
    result = dispatcher.coerce_operands(["  3.14"], float)
    assert result == [3.14]


def test_coerce_operands_trailing_whitespace(dispatcher):
    """coerce_operands handles strings with trailing whitespace."""
    result = dispatcher.coerce_operands(["3.14  "], float)
    assert result == [3.14]


def test_coerce_operands_empty_list(dispatcher):
    """coerce_operands returns empty list when given empty input."""
    result = dispatcher.coerce_operands([], float)
    assert result == []


# ===========================================================================
# coerce_operands: ValueError on Invalid Input
# ===========================================================================


def test_coerce_operands_non_numeric_string_float(dispatcher):
    """coerce_operands raises ValueError for non-numeric string with float coerce."""
    with pytest.raises(ValueError, match="Invalid operand 'abc': expected a numeric value"):
        dispatcher.coerce_operands(["abc"], float)


def test_coerce_operands_non_numeric_string_int(dispatcher):
    """coerce_operands raises ValueError for non-numeric string with int coerce."""
    with pytest.raises(ValueError, match="Invalid operand 'xyz': expected a numeric value"):
        dispatcher.coerce_operands(["xyz"], int)


def test_coerce_operands_empty_string(dispatcher):
    """coerce_operands raises ValueError for empty string."""
    with pytest.raises(ValueError, match="Invalid operand '': expected a numeric value"):
        dispatcher.coerce_operands([""], float)


def test_coerce_operands_only_whitespace(dispatcher):
    """coerce_operands raises ValueError for whitespace-only string."""
    with pytest.raises(ValueError, match="Invalid operand"):
        dispatcher.coerce_operands(["   "], float)


def test_coerce_operands_float_string_to_int(dispatcher):
    """coerce_operands raises ValueError when converting float string with int coerce."""
    with pytest.raises(ValueError, match="Invalid operand '3.14': expected a numeric value"):
        dispatcher.coerce_operands(["3.14"], int)


def test_coerce_operands_special_characters(dispatcher):
    """coerce_operands raises ValueError for strings with special characters."""
    with pytest.raises(ValueError, match="Invalid operand"):
        dispatcher.coerce_operands(["3@14"], float)


def test_coerce_operands_fails_on_first_invalid(dispatcher):
    """coerce_operands raises ValueError on first invalid element, not processing later ones."""
    with pytest.raises(ValueError, match="Invalid operand 'bad'"):
        dispatcher.coerce_operands(["5", "bad", "10"], float)


def test_coerce_operands_inf_string(dispatcher):
    """coerce_operands can convert 'inf' to float infinity."""
    result = dispatcher.coerce_operands(["inf"], float)
    assert result[0] == float("inf")


def test_coerce_operands_negative_inf_string(dispatcher):
    """coerce_operands can convert '-inf' to negative infinity."""
    result = dispatcher.coerce_operands(["-inf"], float)
    assert result[0] == float("-inf")


# ===========================================================================
# coerce_operands: Edge Cases with Callables
# ===========================================================================


def test_coerce_operands_custom_coerce_callable(dispatcher):
    """coerce_operands accepts a custom coerce callable."""
    def custom_coerce(s):
        return int(s) * 2

    result = dispatcher.coerce_operands(["5"], custom_coerce)
    assert result == [10]


def test_coerce_operands_custom_coerce_raises_exception(dispatcher):
    """coerce_operands propagates ValueError from custom coerce callable."""
    def bad_coerce(s):
        raise ValueError("Custom error")

    with pytest.raises(ValueError, match="Invalid operand '5'"):
        dispatcher.coerce_operands(["5"], bad_coerce)


def test_coerce_operands_custom_coerce_raises_type_error(dispatcher):
    """coerce_operands converts TypeError from coerce to ValueError."""
    def bad_coerce(s):
        raise TypeError("Type mismatch")

    with pytest.raises(ValueError, match="Invalid operand '5'"):
        dispatcher.coerce_operands(["5"], bad_coerce)


# ===========================================================================
# dispatch: All 12 Operations - Happy Path
# ===========================================================================


def test_dispatch_add(dispatcher):
    """dispatch calls add(5, 7) and returns 12.0."""
    result = dispatcher.dispatch("add", [5, 7])
    assert result == 12.0


def test_dispatch_subtract(dispatcher):
    """dispatch calls subtract(10, 3) and returns 7.0."""
    result = dispatcher.dispatch("subtract", [10, 3])
    assert result == 7.0


def test_dispatch_multiply(dispatcher):
    """dispatch calls multiply(4, 6) and returns 24.0."""
    result = dispatcher.dispatch("multiply", [4, 6])
    assert result == 24.0


def test_dispatch_divide(dispatcher):
    """dispatch calls divide(10, 2) and returns 5.0."""
    result = dispatcher.dispatch("divide", [10, 2])
    assert result == 5.0


def test_dispatch_power(dispatcher):
    """dispatch calls power(2, 10) and returns 1024.0."""
    result = dispatcher.dispatch("power", [2, 10])
    assert result == 1024.0


def test_dispatch_factorial(dispatcher):
    """dispatch calls factorial(5) and returns 120."""
    result = dispatcher.dispatch("factorial", [5])
    assert result == 120


def test_dispatch_square(dispatcher):
    """dispatch calls square(4) and returns 16.0."""
    result = dispatcher.dispatch("square", [4])
    assert result == 16.0


def test_dispatch_cube(dispatcher):
    """dispatch calls cube(3) and returns 27.0."""
    result = dispatcher.dispatch("cube", [3])
    assert result == 27.0


def test_dispatch_square_root(dispatcher):
    """dispatch calls square_root(9) and returns 3.0."""
    result = dispatcher.dispatch("square_root", [9])
    assert result == 3.0


def test_dispatch_cube_root(dispatcher):
    """dispatch calls cube_root(8) and returns 2.0."""
    result = dispatcher.dispatch("cube_root", [8])
    assert result == 2.0


def test_dispatch_log10(dispatcher):
    """dispatch calls log10(100) and returns 2.0."""
    result = dispatcher.dispatch("log10", [100])
    assert result == 2.0


def test_dispatch_ln(dispatcher):
    """dispatch calls ln(math.e) and returns approximately 1.0."""
    result = dispatcher.dispatch("ln", [math.e])
    assert abs(result - 1.0) < 1e-10


# ===========================================================================
# dispatch: ZeroDivisionError Propagation
# ===========================================================================


def test_dispatch_divide_by_zero_raises(dispatcher):
    """dispatch propagates ZeroDivisionError from divide(1, 0)."""
    with pytest.raises(ZeroDivisionError):
        dispatcher.dispatch("divide", [1, 0])


def test_dispatch_divide_zero_by_zero_raises(dispatcher):
    """dispatch propagates ZeroDivisionError from divide(0, 0)."""
    with pytest.raises(ZeroDivisionError):
        dispatcher.dispatch("divide", [0, 0])


# ===========================================================================
# dispatch: ValueError Propagation (Domain Errors)
# ===========================================================================


def test_dispatch_factorial_negative_raises(dispatcher):
    """dispatch propagates ValueError from factorial(-1)."""
    with pytest.raises(ValueError, match="not defined for negative"):
        dispatcher.dispatch("factorial", [-1])


def test_dispatch_square_root_negative_raises(dispatcher):
    """dispatch propagates ValueError from square_root(-4)."""
    with pytest.raises(ValueError, match="not defined for negative"):
        dispatcher.dispatch("square_root", [-4])


def test_dispatch_log10_negative_raises(dispatcher):
    """dispatch propagates ValueError from log10(-1)."""
    with pytest.raises(ValueError):
        dispatcher.dispatch("log10", [-1])


def test_dispatch_ln_negative_raises(dispatcher):
    """dispatch propagates ValueError from ln(-1)."""
    with pytest.raises(ValueError):
        dispatcher.dispatch("ln", [-1])


def test_dispatch_log10_zero_raises(dispatcher):
    """dispatch propagates ValueError from log10(0)."""
    with pytest.raises(ValueError):
        dispatcher.dispatch("log10", [0])


def test_dispatch_ln_zero_raises(dispatcher):
    """dispatch propagates ValueError from ln(0)."""
    with pytest.raises(ValueError):
        dispatcher.dispatch("ln", [0])


# ===========================================================================
# dispatch: TypeError Propagation (Type Errors)
# ===========================================================================


def test_dispatch_factorial_bool_raises(dispatcher):
    """dispatch propagates TypeError from factorial(True)."""
    with pytest.raises(TypeError, match="does not accept boolean"):
        dispatcher.dispatch("factorial", [True])


def test_dispatch_factorial_float_raises(dispatcher):
    """dispatch propagates TypeError from factorial(3.14)."""
    with pytest.raises(TypeError, match="only accepts non-negative integers"):
        dispatcher.dispatch("factorial", [3.14])


# ===========================================================================
# dispatch: With Negative Operands (Happy Path)
# ===========================================================================


def test_dispatch_add_negatives(dispatcher):
    """dispatch handles negative operands for add."""
    result = dispatcher.dispatch("add", [-5, -3])
    assert result == -8.0


def test_dispatch_multiply_negatives(dispatcher):
    """dispatch handles negative operands for multiply."""
    result = dispatcher.dispatch("multiply", [-4, -6])
    assert result == 24.0


def test_dispatch_square_negative(dispatcher):
    """dispatch handles negative operand for square."""
    result = dispatcher.dispatch("square", [-5])
    assert result == 25.0


def test_dispatch_cube_negative(dispatcher):
    """dispatch handles negative operand for cube."""
    result = dispatcher.dispatch("cube", [-3])
    assert result == -27.0


# ===========================================================================
# dispatch: With Zero Operands (Happy Path)
# ===========================================================================


def test_dispatch_add_zero(dispatcher):
    """dispatch handles zero operands for add."""
    result = dispatcher.dispatch("add", [0, 0])
    assert result == 0.0


def test_dispatch_multiply_by_zero(dispatcher):
    """dispatch handles zero operand for multiply."""
    result = dispatcher.dispatch("multiply", [5, 0])
    assert result == 0.0


def test_dispatch_square_zero(dispatcher):
    """dispatch handles zero for square."""
    result = dispatcher.dispatch("square", [0])
    assert result == 0.0


def test_dispatch_factorial_zero(dispatcher):
    """dispatch handles factorial(0) which returns 1."""
    result = dispatcher.dispatch("factorial", [0])
    assert result == 1


# ===========================================================================
# dispatch: With Large Numbers
# ===========================================================================


def test_dispatch_add_large_numbers(dispatcher):
    """dispatch handles very large numbers."""
    result = dispatcher.dispatch("add", [10**18, 10**18])
    assert result == 2 * 10**18


def test_dispatch_factorial_large_int(dispatcher):
    """dispatch handles factorial(20) correctly."""
    result = dispatcher.dispatch("factorial", [20])
    assert result == math.factorial(20)


# ===========================================================================
# dispatch: Correct Method Resolution (getattr behavior)
# ===========================================================================


def test_dispatch_uses_getattr_correctly(dispatcher):
    """dispatch uses getattr to resolve method names from Calculator."""
    # Verify that getattr is finding the actual methods
    result = dispatcher.dispatch("add", [3, 4])
    assert result == 7.0


def test_dispatch_with_mock_calculator():
    """dispatch can be tested with mock Calculator methods."""
    mock_calc = Mock(spec=Calculator)
    mock_calc.add = Mock(return_value=99.0)

    dispatcher = OperationDispatcher(mock_calc)
    result = dispatcher.dispatch("add", [1, 2])

    assert result == 99.0
    mock_calc.add.assert_called_once_with(1, 2)


# ===========================================================================
# dispatch: Exception Messages Preserved
# ===========================================================================


def test_dispatch_preserves_exception_message(dispatcher):
    """dispatch propagates the original exception message from Calculator."""
    with pytest.raises(ValueError, match="factorial"):
        dispatcher.dispatch("factorial", [-5])


def test_dispatch_preserves_zero_division_message(dispatcher):
    """dispatch propagates ZeroDivisionError from divide."""
    with pytest.raises(ZeroDivisionError):
        dispatcher.dispatch("divide", [1, 0])


# ===========================================================================
# dispatch: Operand Arity Edge Cases
# ===========================================================================


def test_dispatch_binary_operation_with_floats(dispatcher):
    """dispatch handles binary operations with float operands."""
    result = dispatcher.dispatch("divide", [10.5, 2.5])
    assert result == 4.2


def test_dispatch_unary_operation_with_float(dispatcher):
    """dispatch handles unary operations with float operands."""
    result = dispatcher.dispatch("square", [2.5])
    assert result == 6.25


# ===========================================================================
# Integration: coerce_operands -> dispatch pipeline
# ===========================================================================


def test_coerce_then_dispatch_add(dispatcher):
    """Full pipeline: coerce strings, then dispatch add operation."""
    operands = dispatcher.coerce_operands(["5", "7"], float)
    result = dispatcher.dispatch("add", operands)
    assert result == 12.0


def test_coerce_then_dispatch_factorial(dispatcher):
    """Full pipeline: coerce int strings, then dispatch factorial."""
    operands = dispatcher.coerce_operands(["5"], int)
    result = dispatcher.dispatch("factorial", operands)
    assert result == 120


def test_coerce_then_dispatch_with_invalid_raises(dispatcher):
    """Full pipeline: coerce raises ValueError before dispatch is called."""
    with pytest.raises(ValueError, match="Invalid operand 'bad'"):
        operands = dispatcher.coerce_operands(["bad"], float)
        # dispatch should never be reached
        dispatcher.dispatch("add", operands)
