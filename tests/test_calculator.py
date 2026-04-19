import pytest
import math
from src.calculator import Calculator


def test_divide_integer_by_zero_raises_error():
    """Test that dividing an integer by zero raises ZeroDivisionError."""
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(10, 0)


def test_divide_float_by_zero_raises_error():
    """Test that dividing a float by zero raises ZeroDivisionError."""
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(10.5, 0.0)


def test_divide_negative_by_zero_raises_error():
    """Test that dividing a negative number by zero raises ZeroDivisionError."""
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(-5, 0)


def test_divide_normal_division_works():
    """Test that normal division still works correctly."""
    calc = Calculator()
    result = calc.divide(10, 2)
    assert result == 5.0