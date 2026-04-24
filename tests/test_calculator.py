import pytest
import math
from src.calculator import Calculator


@pytest.fixture
def calculator():
    """Fixture providing a Calculator instance for tests."""
    return Calculator()


class TestDivide:
    """Test suite for the divide method."""

    def test_divide_by_zero(self, calculator):
        """Test that dividing by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(10, 0)

    def test_divide_zero_by_number(self, calculator):
        """Test that 0 divided by a number returns 0."""
        result = calculator.divide(0, 5)
        assert result == 0

    def test_divide_zero_by_negative_number(self, calculator):
        """Test that 0 divided by a negative number returns 0."""
        result = calculator.divide(0, -5)
        assert result == 0

    def test_divide_negative_by_positive(self, calculator):
        """Test that a negative number divided by a positive number returns a negative result."""
        result = calculator.divide(-10, 5)
        assert result == -2.0

    def test_divide_positive_by_negative(self, calculator):
        """Test that a positive number divided by a negative number returns a negative result."""
        result = calculator.divide(10, -5)
        assert result == -2.0

    def test_divide_negative_by_negative(self, calculator):
        """Test that a negative number divided by a negative number returns a positive result."""
        result = calculator.divide(-10, -5)
        assert result == 2.0

    def test_divide_normal_case(self, calculator):
        """Test normal division with positive integers."""
        result = calculator.divide(10, 2)
        assert result == 5.0

    def test_divide_fractional_result(self, calculator):
        """Test that division can produce fractional results."""
        result = calculator.divide(7, 2)
        assert result == 3.5