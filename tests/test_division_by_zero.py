import pytest
from src.calculator import Calculator


@pytest.fixture
def calculator():
    """Fixture providing a Calculator instance for each test."""
    return Calculator()


class TestDivisionByZero:
    """Tests for division-by-zero edge cases in the Calculator.divide() method."""

    def test_divide_by_zero_integer(self, calculator):
        """Test that dividing an integer by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(10, 0)

    def test_divide_by_zero_float(self, calculator):
        """Test that dividing a float by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(3.14, 0)

    def test_divide_zero_by_zero(self, calculator):
        """Test that zero divided by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(0, 0)

    def test_divide_negative_by_zero(self, calculator):
        """Test that dividing a negative number by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(-5, 0)

    def test_divide_negative_float_by_zero(self, calculator):
        """Test that dividing a negative float by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(-2.71, 0)

    def test_divide_zero_by_zero_float(self, calculator):
        """Test that zero (float) divided by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(0.0, 0.0)

    def test_divide_positive_integer_by_positive_integer(self, calculator):
        """Regression test: dividing positive integers with non-zero divisor returns correct result."""
        result = calculator.divide(10, 2)
        assert result == 5

    def test_divide_positive_float_by_positive_float(self, calculator):
        """Regression test: dividing positive floats with non-zero divisor returns correct result."""
        result = calculator.divide(7.5, 2.5)
        assert result == 3.0

    def test_divide_positive_by_negative(self, calculator):
        """Regression test: dividing positive by negative returns correct negative result."""
        result = calculator.divide(10, -2)
        assert result == -5

    def test_divide_negative_by_positive(self, calculator):
        """Regression test: dividing negative by positive returns correct negative result."""
        result = calculator.divide(-10, 2)
        assert result == -5

    def test_divide_negative_by_negative(self, calculator):
        """Regression test: dividing negative by negative returns correct positive result."""
        result = calculator.divide(-10, -2)
        assert result == 5

    def test_divide_zero_by_positive_integer(self, calculator):
        """Regression test: zero divided by positive integer returns zero."""
        result = calculator.divide(0, 5)
        assert result == 0

    def test_divide_zero_by_negative_integer(self, calculator):
        """Regression test: zero divided by negative integer returns zero."""
        result = calculator.divide(0, -5)
        assert result == 0

    def test_divide_fractional_result(self, calculator):
        """Regression test: dividing integers that don't divide evenly returns float."""
        result = calculator.divide(5, 2)
        assert result == 2.5

    def test_divide_by_float_divisor(self, calculator):
        """Regression test: dividing by float divisor returns correct result."""
        result = calculator.divide(10, 0.5)
        assert result == 20
