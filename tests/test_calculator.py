import pytest
import math
from src.calculator import Calculator


def test_divide_by_zero():
    calculator = Calculator()
    with pytest.raises(ZeroDivisionError):
        calculator.divide(1, 0)
