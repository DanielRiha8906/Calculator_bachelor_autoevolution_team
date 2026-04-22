import pytest
import math
from src.calculator import Calculator


class TestCalculatorDivide:
    """Test cases for the Calculator.divide() method."""

    def test_divide_positive_by_positive(self):
        """Test normal division: positive number divided by positive number."""
        calc = Calculator()
        result = calc.divide(10, 2)
        assert result == 5

    def test_divide_positive_by_positive_float(self):
        """Test division with floating point results."""
        calc = Calculator()
        result = calc.divide(5, 2)
        assert result == 2.5

    def test_divide_negative_by_positive(self):
        """Test division: negative number divided by positive number."""
        calc = Calculator()
        result = calc.divide(-10, 2)
        assert result == -5

    def test_divide_positive_by_negative(self):
        """Test division: positive number divided by negative number."""
        calc = Calculator()
        result = calc.divide(10, -2)
        assert result == -5

    def test_divide_negative_by_negative(self):
        """Test division: negative number divided by negative number."""
        calc = Calculator()
        result = calc.divide(-10, -2)
        assert result == 5

    def test_divide_zero_by_positive(self):
        """Test division: zero divided by positive number."""
        calc = Calculator()
        result = calc.divide(0, 5)
        assert result == 0

    def test_divide_zero_by_negative(self):
        """Test division: zero divided by negative number."""
        calc = Calculator()
        result = calc.divide(0, -5)
        assert result == 0

    def test_divide_by_zero_positive_numerator(self):
        """Test that dividing positive number by zero raises ZeroDivisionError."""
        calc = Calculator()
        with pytest.raises(ZeroDivisionError):
            calc.divide(5, 0)

    def test_divide_by_zero_float_numerator(self):
        """Test that dividing float by zero raises ZeroDivisionError."""
        calc = Calculator()
        with pytest.raises(ZeroDivisionError):
            calc.divide(5.0, 0)

    def test_divide_by_zero_zero_numerator(self):
        """Test that 0 divided by 0 raises ZeroDivisionError."""
        calc = Calculator()
        with pytest.raises(ZeroDivisionError):
            calc.divide(0, 0)

    def test_divide_by_zero_negative_numerator(self):
        """Test that dividing negative number by zero raises ZeroDivisionError."""
        calc = Calculator()
        with pytest.raises(ZeroDivisionError):
            calc.divide(-3, 0)

    def test_divide_large_numbers(self):
        """Test division with large numbers."""
        calc = Calculator()
        result = calc.divide(1000000, 1000)
        assert result == 1000

    def test_divide_very_small_result(self):
        """Test division resulting in very small float."""
        calc = Calculator()
        result = calc.divide(1, 1000000)
        assert abs(result - 0.000001) < 1e-10

    @pytest.mark.parametrize("numerator,denominator,expected", [
        (10, 2, 5),
        (15, 3, 5),
        (20, 4, 5),
        (100, 10, 10),
    ])
    def test_divide_parametrized_valid(self, numerator, denominator, expected):
        """Parametrized test for valid division cases."""
        calc = Calculator()
        result = calc.divide(numerator, denominator)
        assert result == expected

    @pytest.mark.parametrize("numerator", [5, 5.0, 0, -3, -10, 1000000])
    def test_divide_by_zero_parametrized(self, numerator):
        """Parametrized test for division by zero with various numerators."""
        calc = Calculator()
        with pytest.raises(ZeroDivisionError):
            calc.divide(numerator, 0)