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


class TestCalculatorFactorial:
    """Test suite for Calculator.factorial() method."""

    def test_factorial_zero(self, calculator):
        """Verify factorial of zero returns 1."""
        result = calculator.factorial(0)
        assert result == 1

    def test_factorial_one(self, calculator):
        """Verify factorial of one returns 1."""
        result = calculator.factorial(1)
        assert result == 1

    def test_factorial_small_positive(self, calculator):
        """Verify factorial of small positive integer."""
        result = calculator.factorial(5)
        assert result == 120

    def test_factorial_moderate_positive(self, calculator):
        """Verify factorial of moderate positive integer."""
        result = calculator.factorial(10)
        assert result == 3628800

    def test_factorial_twenty(self, calculator):
        """Verify factorial of twenty."""
        result = calculator.factorial(20)
        assert result == 2432902008176640000

    def test_factorial_negative_raises_error(self, calculator):
        """Verify that factorial of negative integer raises ValueError."""
        with pytest.raises(ValueError):
            calculator.factorial(-1)

    def test_factorial_negative_five_raises_error(self, calculator):
        """Verify that factorial of -5 raises ValueError."""
        with pytest.raises(ValueError):
            calculator.factorial(-5)

    def test_factorial_float_raises_error(self, calculator):
        """Verify that factorial of float raises ValueError."""
        with pytest.raises(ValueError):
            calculator.factorial(5.5)

    def test_factorial_string_raises_error(self, calculator):
        """Verify that factorial of string raises ValueError."""
        with pytest.raises(ValueError):
            calculator.factorial("5")

    def test_factorial_none_raises_error(self, calculator):
        """Verify that factorial of None raises ValueError."""
        with pytest.raises(ValueError):
            calculator.factorial(None)