import pytest
import math
from src.calculator import Calculator


def test_divide_by_zero():
    calc = Calculator()
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        calc.divide(10, 0)


def test_divide_by_float_zero_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        calc.divide(10, 0.0)


def test_divide_negative_numerator_by_zero_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        calc.divide(-5, 0)


def test_divide_zero_by_zero_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        calc.divide(0, 0)


def test_divide_normal_case_returns_correct_result():
    calc = Calculator()
    result = calc.divide(10, 2)
    assert result == 5.0


def test_divide_zero_numerator_nonzero_denominator_returns_zero():
    calc = Calculator()
    result = calc.divide(0, 5)
    assert result == 0.0