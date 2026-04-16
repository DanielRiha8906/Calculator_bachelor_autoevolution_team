import pytest
import math
from src.calculator import Calculator


def test_divide_by_zero_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        calc.divide(10, 0)


def test_divide_happy_path():
    calc = Calculator()
    assert calc.divide(10, 5) == 2.0