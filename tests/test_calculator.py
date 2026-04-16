import pytest
import math
from src.calculator import Calculator


def test_divide_by_zero():
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(1, 0)
    with pytest.raises(ZeroDivisionError):
        calc.divide(-5, 0)


@pytest.mark.parametrize("numerator,denominator", [
    (1, 0.0),       # float zero denominator
    (1.0, 0.0),     # both floats, zero denominator
    (1, 0j),        # complex zero denominator
])
def test_divide_by_zero_alternate_zero_types(numerator, denominator):
    """Verify ZeroDivisionError is raised for non-integer representations of zero as divisor."""
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(numerator, denominator)