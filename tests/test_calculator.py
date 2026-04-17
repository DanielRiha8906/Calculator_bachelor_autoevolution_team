import pytest
import math
from src.calculator import Calculator


def test_divide_valid():
    calc = Calculator()
    assert calc.divide(10, 2) == 5.0

def test_divide_by_zero():
    calc = Calculator()
    with pytest.raises(ValueError, match="zero"):
        calc.divide(5, 0)


# --- Edge-case tests for Calculator.divide ---

def test_divide_negative_numerator():
    calc = Calculator()
    result = calc.divide(-10, 2)
    assert result == -5.0


def test_divide_negative_denominator():
    calc = Calculator()
    result = calc.divide(10, -2)
    assert result == -5.0


def test_divide_both_negative():
    calc = Calculator()
    result = calc.divide(-10, -2)
    assert result == 5.0


def test_divide_zero_numerator():
    calc = Calculator()
    result = calc.divide(0, 5)
    assert result == 0.0


def test_divide_zero_numerator_float():
    calc = Calculator()
    result = calc.divide(0.0, 5)
    assert result == 0.0


def test_divide_float_inputs():
    calc = Calculator()
    result = calc.divide(7.5, 2.5)
    assert math.isclose(result, 3.0)


def test_divide_float_numerator_int_denominator():
    calc = Calculator()
    result = calc.divide(1.0, 3)
    assert math.isclose(result, 1.0 / 3)


def test_divide_by_zero_float():
    calc = Calculator()
    with pytest.raises(ValueError, match="zero"):
        calc.divide(5, 0.0)


def test_divide_very_large_numbers():
    calc = Calculator()
    result = calc.divide(10**18, 10**9)
    assert result == 10**9


def test_divide_very_large_by_very_large():
    calc = Calculator()
    result = calc.divide(10**300, 10**300)
    assert result == 1.0


def test_divide_result_is_float():
    calc = Calculator()
    result = calc.divide(1, 3)
    assert isinstance(result, float)


def test_divide_negative_zero_float_denominator():
    # -0.0 is equal to 0.0 in Python; the guard must catch it
    calc = Calculator()
    with pytest.raises(ValueError, match="zero"):
        calc.divide(5, -0.0)


@pytest.mark.parametrize("a, b, expected", [
    (9, 3, 3.0),
    (-9, 3, -3.0),
    (9, -3, -3.0),
    (-9, -3, 3.0),
    (0, 1, 0.0),
    (1, 1, 1.0),
    (100, 4, 25.0),
])
def test_divide_parametrized(a, b, expected):
    calc = Calculator()
    assert calc.divide(a, b) == expected