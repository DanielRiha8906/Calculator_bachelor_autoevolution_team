import pytest
import math
from src.calculator import Calculator


def test_divide_by_zero():
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(1, 0)


def test_divide_by_false():
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(1, False)


@pytest.mark.parametrize("b", ["string", None])
def test_divide_by_non_numeric(b):
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.divide(1, b)


def test_divide_by_infinity():
    calc = Calculator()
    result = calc.divide(1.0, float('inf'))
    assert result == 0.0


def test_divide_by_nan():
    calc = Calculator()
    result = calc.divide(1.0, float('nan'))
    assert math.isnan(result)