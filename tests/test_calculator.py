import pytest
import math
from src.calculator import Calculator


@pytest.fixture
def calc():
    """Fixture providing a Calculator instance."""
    return Calculator()


def test_division_by_zero(calc):
    """Verify that dividing by zero raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        calc.divide(10, 0)


def test_division_by_zero_zero_numerator(calc):
    """Verify that 0/0 also raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        calc.divide(0, 0)


def test_division_normal(calc):
    """Verify normal division works correctly (regression check)."""
    result = calc.divide(10, 2)
    assert result == 5.0