import pytest
import math
from src.calculator import Calculator


@pytest.fixture
def calc():
    """Fixture to provide a Calculator instance."""
    return Calculator()


def test_divide_by_zero_integer(calc):
    """Test that dividing by zero with integer raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        calc.divide(10, 0)


def test_divide_by_zero_float(calc):
    """Test that dividing by zero with float raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        calc.divide(10.5, 0.0)


def test_divide_by_zero_mixed(calc):
    """Test that dividing by zero with mixed int/float raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        calc.divide(7, 0.0)