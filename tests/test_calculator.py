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


class TestFactorial:
    """Test suite for the factorial method."""

    def test_factorial_zero(self, calculator):
        """Test that factorial of zero returns 1."""
        result = calculator.factorial(0)
        assert result == 1

    def test_factorial_one(self, calculator):
        """Test that factorial of one returns 1."""
        result = calculator.factorial(1)
        assert result == 1

    def test_factorial_small_positive_integer(self, calculator):
        """Test factorial of a small positive integer (5)."""
        result = calculator.factorial(5)
        assert result == 120

    def test_factorial_larger_positive_integer(self, calculator):
        """Test factorial of a larger positive integer (10)."""
        result = calculator.factorial(10)
        assert result == 3628800

    def test_factorial_large_positive_integer(self, calculator):
        """Test factorial of a large positive integer (100)."""
        result = calculator.factorial(100)
        assert result == math.factorial(100)

    @pytest.mark.parametrize("negative_input", [-1, -5])
    def test_factorial_negative_integer(self, calculator, negative_input):
        """Test that factorial of negative integers raises ValueError."""
        with pytest.raises(ValueError):
            calculator.factorial(negative_input)

    @pytest.mark.parametrize("invalid_input", [2.5, 5.0, "5", None])
    def test_factorial_invalid_input_types(self, calculator, invalid_input):
        """Test that factorial with invalid input types raises TypeError or ValueError."""
        with pytest.raises((TypeError, ValueError)):
            calculator.factorial(invalid_input)