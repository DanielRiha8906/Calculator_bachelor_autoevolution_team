import pytest
import math
from src.calculator import Calculator


@pytest.fixture
def calc():
    """Fixture to provide a Calculator instance for all tests."""
    return Calculator()


class TestDivide:
    """Test suite for the Calculator.divide() method."""

    def test_divide_by_zero(self, calc):
        """Verify that dividing by zero (int) raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calc.divide(5, 0)

    def test_divide_by_zero_float(self, calc):
        """Verify that dividing by zero (float) raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calc.divide(5, 0.0)

    def test_divide_invalid_type_numerator(self, calc):
        """Verify that TypeError is raised when numerator is a string."""
        with pytest.raises(TypeError):
            calc.divide("a", 2)

    def test_divide_invalid_type_denominator(self, calc):
        """Verify that TypeError is raised when denominator is a string."""
        with pytest.raises(TypeError):
            calc.divide(2, "b")

    def test_divide_invalid_type_none(self, calc):
        """Verify that TypeError is raised when denominator is None."""
        with pytest.raises(TypeError):
            calc.divide(5, None)

    # Additional edge cases and comprehensive coverage

    def test_divide_invalid_type_numerator_none(self, calc):
        """Verify that TypeError is raised when numerator is None."""
        with pytest.raises(TypeError):
            calc.divide(None, 5)

    def test_divide_both_none(self, calc):
        """Verify that TypeError is raised when both operands are None."""
        with pytest.raises(TypeError):
            calc.divide(None, None)

    def test_divide_numerator_list(self, calc):
        """Verify that TypeError is raised when numerator is a list."""
        with pytest.raises(TypeError):
            calc.divide([1, 2], 2)

    def test_divide_denominator_list(self, calc):
        """Verify that TypeError is raised when denominator is a list."""
        with pytest.raises(TypeError):
            calc.divide(10, [2])

    def test_divide_numerator_dict(self, calc):
        """Verify that TypeError is raised when numerator is a dict."""
        with pytest.raises(TypeError):
            calc.divide({"a": 1}, 2)

    def test_divide_denominator_dict(self, calc):
        """Verify that TypeError is raised when denominator is a dict."""
        with pytest.raises(TypeError):
            calc.divide(10, {"a": 2})

    def test_divide_happy_path_int(self, calc):
        """Verify normal division with positive integers."""
        result = calc.divide(10, 2)
        assert result == 5.0

    def test_divide_happy_path_float(self, calc):
        """Verify normal division with floats."""
        result = calc.divide(10.5, 2.5)
        assert abs(result - 4.2) < 1e-10

    def test_divide_negative_dividend(self, calc):
        """Verify division with negative dividend."""
        result = calc.divide(-10, 2)
        assert result == -5.0

    def test_divide_negative_divisor(self, calc):
        """Verify division with negative divisor."""
        result = calc.divide(10, -2)
        assert result == -5.0

    def test_divide_both_negative(self, calc):
        """Verify division with both operands negative."""
        result = calc.divide(-10, -2)
        assert result == 5.0

    def test_divide_fractional_result(self, calc):
        """Verify division that results in a non-integer quotient."""
        result = calc.divide(7, 3)
        assert abs(result - 7/3) < 1e-10

    def test_divide_by_one(self, calc):
        """Verify division by one returns the original number."""
        result = calc.divide(42, 1)
        assert result == 42.0

    def test_divide_zero_by_nonzero(self, calc):
        """Verify that zero divided by a non-zero number returns zero."""
        result = calc.divide(0, 5)
        assert result == 0.0

    def test_divide_zero_by_negative(self, calc):
        """Verify that zero divided by a negative number returns zero."""
        result = calc.divide(0, -5)
        assert result == 0.0

    def test_divide_very_large_numbers(self, calc):
        """Verify division with very large numbers."""
        result = calc.divide(1e100, 1e50)
        assert abs(result - 1e50) < 1e40

    def test_divide_very_small_numbers(self, calc):
        """Verify division with very small positive numbers."""
        result = calc.divide(1e-10, 1e-5)
        assert abs(result - 1e-5) < 1e-15

    def test_divide_mixed_int_float(self, calc):
        """Verify division with mixed integer and float operands."""
        result = calc.divide(10, 2.5)
        assert result == 4.0

    def test_divide_mixed_float_int(self, calc):
        """Verify division with float and integer operands (reversed)."""
        result = calc.divide(10.5, 2)
        assert abs(result - 5.25) < 1e-10

    def test_divide_infinity_numerator(self, calc):
        """Verify division when numerator is infinity."""
        result = calc.divide(float('inf'), 2)
        assert result == float('inf')

    def test_divide_infinity_denominator(self, calc):
        """Verify division when denominator is infinity."""
        result = calc.divide(10, float('inf'))
        assert result == 0.0

    def test_divide_infinity_both(self, calc):
        """Verify division when both are infinity results in NaN."""
        result = calc.divide(float('inf'), float('inf'))
        assert math.isnan(result)

    def test_divide_nan_numerator(self, calc):
        """Verify division when numerator is NaN."""
        result = calc.divide(float('nan'), 2)
        assert math.isnan(result)

    def test_divide_nan_denominator(self, calc):
        """Verify division when denominator is NaN."""
        result = calc.divide(10, float('nan'))
        assert math.isnan(result)

    def test_divide_zero_zero(self, calc):
        """Verify that zero divided by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calc.divide(0, 0)