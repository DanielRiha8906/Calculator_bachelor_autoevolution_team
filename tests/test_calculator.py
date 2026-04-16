import pytest
import math
from src.calculator import Calculator


def test_divide_by_zero():
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(1, 0)


@pytest.mark.parametrize("divisor", [
    0.0,   # float positive zero
    -0.0,  # IEEE 754 negative zero — distinct bit pattern but still zero
])
def test_divide_by_float_zero_raises(divisor):
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(1, divisor)
