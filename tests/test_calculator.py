import pytest
import math
from src.calculator import Calculator

def test_divide_by_zero_raises_zero_division_error():
    with pytest.raises(ZeroDivisionError):
        Calculator().divide(1, 0)


@pytest.mark.parametrize("numerator, divisor", [
    (1,   0.0),   # float zero divisor
    (0,   0),     # zero divided by zero (integer)
    (-1,  0),     # negative numerator, integer zero
    (-5,  0.0),   # negative numerator, float zero divisor
])
def test_divide_by_zero_variants_raise_zero_division_error(numerator, divisor):
    """ZeroDivisionError must be raised for all zero-divisor variants."""
    with pytest.raises(ZeroDivisionError):
        Calculator().divide(numerator, divisor)