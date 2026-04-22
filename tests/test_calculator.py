import pytest
import math
from src.calculator import Calculator


class TestDivideByZero:
    """Test division by zero exception handling."""

    def test_divide_by_zero_with_positive_integer(self):
        """Verify ZeroDivisionError is raised when dividing positive integer by zero."""
        calculator = Calculator()
        with pytest.raises(ZeroDivisionError):
            calculator.divide(10, 0)

    def test_divide_by_zero_with_negative_integer(self):
        """Verify ZeroDivisionError is raised when dividing negative integer by zero."""
        calculator = Calculator()
        with pytest.raises(ZeroDivisionError):
            calculator.divide(-10, 0)

    def test_divide_by_zero_with_zero(self):
        """Verify ZeroDivisionError is raised when dividing zero by zero."""
        calculator = Calculator()
        with pytest.raises(ZeroDivisionError):
            calculator.divide(0, 0)

    def test_divide_by_zero_with_float(self):
        """Verify ZeroDivisionError is raised when dividing float by zero."""
        calculator = Calculator()
        with pytest.raises(ZeroDivisionError):
            calculator.divide(3.14, 0)

    def test_divide_by_zero_with_large_number(self):
        """Verify ZeroDivisionError is raised when dividing large number by zero."""
        calculator = Calculator()
        with pytest.raises(ZeroDivisionError):
            calculator.divide(999999999, 0)

    def test_divide_by_zero_is_exact_exception_type(self):
        """Verify exception is exactly ZeroDivisionError, not a subclass."""
        calculator = Calculator()
        with pytest.raises(ZeroDivisionError) as exc_info:
            calculator.divide(5, 0)
        # Verify it's the exact type, not a subclass
        assert type(exc_info.value) is ZeroDivisionError


class TestDivideNormalOperation:
    """Test normal division operations (regression tests)."""

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (10, 2, 5.0),
            (20, 4, 5.0),
            (7, 2, 3.5),
            (100, 10, 10.0),
            (1, 1, 1.0),
        ],
    )
    def test_divide_returns_correct_quotient(self, a, b, expected):
        """Verify divide returns correct result for valid inputs."""
        calculator = Calculator()
        result = calculator.divide(a, b)
        assert result == expected

    def test_divide_negative_dividend(self):
        """Verify division works with negative dividend."""
        calculator = Calculator()
        result = calculator.divide(-10, 2)
        assert result == -5.0

    def test_divide_negative_divisor(self):
        """Verify division works with negative divisor."""
        calculator = Calculator()
        result = calculator.divide(10, -2)
        assert result == -5.0

    def test_divide_both_negative(self):
        """Verify division works when both operands are negative."""
        calculator = Calculator()
        result = calculator.divide(-10, -2)
        assert result == 5.0

    def test_divide_zero_dividend(self):
        """Verify dividing zero by non-zero returns zero."""
        calculator = Calculator()
        result = calculator.divide(0, 5)
        assert result == 0.0

    def test_divide_float_operands(self):
        """Verify division works with float operands."""
        calculator = Calculator()
        result = calculator.divide(7.5, 2.5)
        assert result == 3.0

    def test_divide_fractional_result(self):
        """Verify division returns fractional result correctly."""
        calculator = Calculator()
        result = calculator.divide(1, 3)
        assert abs(result - (1 / 3)) < 1e-10

    def test_divide_very_small_divisor(self):
        """Verify division with very small (but non-zero) divisor works."""
        calculator = Calculator()
        result = calculator.divide(1, 1e-10)
        assert result == 1e10

    def test_divide_very_large_dividend(self):
        """Verify division with very large dividend works."""
        calculator = Calculator()
        result = calculator.divide(1e10, 2)
        assert result == 5e9


class TestDivideEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_divide_by_float_zero(self):
        """Verify ZeroDivisionError is raised when dividing by float zero."""
        calculator = Calculator()
        with pytest.raises(ZeroDivisionError):
            calculator.divide(10, 0.0)

    def test_divide_returns_float_type(self):
        """Verify divide always returns float type."""
        calculator = Calculator()
        result = calculator.divide(10, 2)
        assert isinstance(result, float)

    def test_divide_integer_and_float_mixing(self):
        """Verify division works with mixed integer and float types."""
        calculator = Calculator()
        result1 = calculator.divide(10, 2.5)
        result2 = calculator.divide(10.5, 2)
        assert result1 == 4.0
        assert result2 == 5.25