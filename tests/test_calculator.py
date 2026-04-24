import pytest
import math
from src.calculator import Calculator


@pytest.fixture
def calculator():
    """Fixture providing a Calculator instance for tests."""
    return Calculator()


class TestCalculatorAdd:
    """Test suite for Calculator.add() method."""

    def test_addition_positive_integers(self, calculator):
        """Verify addition of positive integers."""
        result = calculator.add(5, 3)
        assert result == 8

    def test_addition_negative_integers(self, calculator):
        """Verify addition of negative integers."""
        result = calculator.add(-5, -3)
        assert result == -8

    def test_addition_mixed_signs(self, calculator):
        """Verify addition with mixed sign operands."""
        result = calculator.add(-5, 8)
        assert result == 3

    def test_addition_with_floats(self, calculator):
        """Verify addition with float operands."""
        result = calculator.add(2.5, 3.5)
        assert result == 6.0

    def test_addition_with_zero(self, calculator):
        """Verify addition with zero as second operand."""
        result = calculator.add(5, 0)
        assert result == 5

    def test_addition_zero_to_zero(self, calculator):
        """Verify addition of zero and zero."""
        result = calculator.add(0, 0)
        assert result == 0


class TestCalculatorSubtract:
    """Test suite for Calculator.subtract() method."""

    def test_subtraction_positive_integers(self, calculator):
        """Verify subtraction of positive integers."""
        result = calculator.subtract(10, 3)
        assert result == 7

    def test_subtraction_negative_result(self, calculator):
        """Verify subtraction resulting in negative value."""
        result = calculator.subtract(3, 10)
        assert result == -7

    def test_subtraction_negative_operands(self, calculator):
        """Verify subtraction with negative operands."""
        result = calculator.subtract(-5, -3)
        assert result == -2

    def test_subtraction_with_floats(self, calculator):
        """Verify subtraction with float operands."""
        result = calculator.subtract(7.5, 2.5)
        assert result == 5.0

    def test_subtraction_with_zero_minuend(self, calculator):
        """Verify subtraction with zero as minuend."""
        result = calculator.subtract(0, 5)
        assert result == -5

    def test_subtraction_with_zero_subtrahend(self, calculator):
        """Verify subtraction with zero as subtrahend."""
        result = calculator.subtract(5, 0)
        assert result == 5


class TestCalculatorMultiply:
    """Test suite for Calculator.multiply() method."""

    def test_multiplication_positive_integers(self, calculator):
        """Verify multiplication of positive integers."""
        result = calculator.multiply(4, 3)
        assert result == 12

    def test_multiplication_negative_integers(self, calculator):
        """Verify multiplication of negative integers."""
        result = calculator.multiply(-4, -3)
        assert result == 12

    def test_multiplication_mixed_signs(self, calculator):
        """Verify multiplication with mixed sign operands."""
        result = calculator.multiply(-4, 3)
        assert result == -12

    def test_multiplication_with_floats(self, calculator):
        """Verify multiplication with float operands."""
        result = calculator.multiply(2.5, 4.0)
        assert result == 10.0

    def test_multiplication_by_zero(self, calculator):
        """Verify multiplication by zero."""
        result = calculator.multiply(5, 0)
        assert result == 0

    def test_multiplication_by_one(self, calculator):
        """Verify multiplication by one."""
        result = calculator.multiply(5, 1)
        assert result == 5


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