import pytest
import math
from src.calculator import Calculator


@pytest.fixture
def calculator():
    """Fixture providing a Calculator instance for tests."""
    return Calculator()


class TestCalculatorDivide:
    """Test suite for Calculator.divide() method."""

    def test_division_by_zero(self, calculator):
        """Verify that dividing by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(10, 0)

    def test_division_normal(self, calculator):
        """Verify correct behavior with positive integer operands."""
        result = calculator.divide(10, 2)
        assert result == 5.0

    def test_division_with_floats(self, calculator):
        """Verify correct behavior with float operands."""
        result = calculator.divide(7.5, 2.5)
        assert result == 3.0

    def test_division_negative_divisor(self, calculator):
        """Verify correct behavior with negative divisor."""
        result = calculator.divide(10, -2)
        assert result == -5.0

    def test_division_zero_dividend(self, calculator):
        """Verify zero numerator is handled correctly."""
        result = calculator.divide(0, 5)
        assert result == 0.0