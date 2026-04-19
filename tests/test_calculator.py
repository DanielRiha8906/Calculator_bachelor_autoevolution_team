import pytest
import math
from src.calculator import Calculator


@pytest.fixture
def calculator():
    """Provides a fresh Calculator instance for each test."""
    return Calculator()


def test_divide_by_zero_integer(calculator):
    """Verify that dividing by zero with integer raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        calculator.divide(10, 0)


def test_divide_by_zero_float(calculator):
    """Verify that dividing by zero with float raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        calculator.divide(10, 0.0)


def test_divide_by_zero_negative_numerator(calculator):
    """Verify that dividing negative numerator by zero raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        calculator.divide(-10, 0)


def test_divide_with_invalid_inputs(calculator):
    """Verify that dividing with invalid inputs (None, string) raises TypeError."""
    # Test with None divisor
    with pytest.raises(TypeError):
        calculator.divide(10, None)

    # Test with string divisor (non-numeric)
    with pytest.raises(TypeError):
        calculator.divide(10, "abc")

    # Test with empty string divisor
    with pytest.raises(TypeError):
        calculator.divide(10, "")