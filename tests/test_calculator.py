import pytest
import math
from src.calculator import Calculator


@pytest.fixture
def calculator():
    """Fixture providing a Calculator instance for tests."""
    return Calculator()


class TestDivideValidInputs:
    """Test divide method with valid numeric inputs."""

    def test_divide_positive_numbers(self, calculator):
        """Verify division works correctly with positive numbers."""
        assert calculator.divide(10, 2) == 5
        assert calculator.divide(7, 2) == 3.5
        assert calculator.divide(1, 1) == 1

    def test_divide_negative_numbers(self, calculator):
        """Verify division works correctly with negative numbers."""
        assert calculator.divide(-10, 2) == -5
        assert calculator.divide(10, -2) == -5
        assert calculator.divide(-10, -2) == 5

    def test_divide_floats(self, calculator):
        """Verify division works correctly with floating-point numbers."""
        assert calculator.divide(7.5, 2.5) == 3.0
        assert calculator.divide(1.0, 3.0) == pytest.approx(0.333333, rel=1e-5)

    def test_divide_zero_numerator(self, calculator):
        """Verify dividing zero by a non-zero number returns zero."""
        assert calculator.divide(0, 5) == 0
        assert calculator.divide(0, -3) == 0
        assert calculator.divide(0, 0.5) == 0


class TestDivideByZero:
    """Test divide method with zero divisor."""

    def test_divide_by_zero_integer(self, calculator):
        """Verify ZeroDivisionError is raised when divisor is 0."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(5, 0)

    def test_divide_by_zero_float(self, calculator):
        """Verify ZeroDivisionError is raised when divisor is 0.0."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(10.5, 0.0)

    def test_divide_zero_by_zero(self, calculator):
        """Verify ZeroDivisionError is raised for 0/0."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(0, 0)


class TestDivideInvalidTypes:
    """Test divide method with non-numeric inputs."""

    def test_divide_string_numerator(self, calculator):
        """Verify TypeError is raised when numerator is a string."""
        with pytest.raises(TypeError):
            calculator.divide("10", 2)

    def test_divide_string_denominator(self, calculator):
        """Verify TypeError is raised when denominator is a string."""
        with pytest.raises(TypeError):
            calculator.divide(10, "2")

    def test_divide_both_strings(self, calculator):
        """Verify TypeError is raised when both arguments are strings."""
        with pytest.raises(TypeError):
            calculator.divide("10", "2")

    def test_divide_list_numerator(self, calculator):
        """Verify TypeError is raised when numerator is a list."""
        with pytest.raises(TypeError):
            calculator.divide([10], 2)

    def test_divide_list_denominator(self, calculator):
        """Verify TypeError is raised when denominator is a list."""
        with pytest.raises(TypeError):
            calculator.divide(10, [2])

    def test_divide_none_numerator(self, calculator):
        """Verify TypeError is raised when numerator is None."""
        with pytest.raises(TypeError):
            calculator.divide(None, 2)

    def test_divide_none_denominator(self, calculator):
        """Verify TypeError is raised when denominator is None."""
        with pytest.raises(TypeError):
            calculator.divide(10, None)

    def test_divide_dict_numerator(self, calculator):
        """Verify TypeError is raised when numerator is a dict."""
        with pytest.raises(TypeError):
            calculator.divide({"value": 10}, 2)

    def test_divide_dict_denominator(self, calculator):
        """Verify TypeError is raised when denominator is a dict."""
        with pytest.raises(TypeError):
            calculator.divide(10, {"value": 2})

    def test_divide_boolean_numerator(self, calculator):
        """Verify division works with boolean (int subclass in Python)."""
        # Note: In Python, bool is a subclass of int, so True=1, False=0
        assert calculator.divide(True, 1) == 1
        assert calculator.divide(False, 1) == 0

    def test_divide_boolean_denominator(self, calculator):
        """Verify division works with boolean denominator (int subclass)."""
        assert calculator.divide(2, True) == 2

    def test_divide_boolean_zero_denominator(self, calculator):
        """Verify ZeroDivisionError when boolean denominator is False."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(2, False)


class TestDivideEdgeCases:
    """Test divide method with edge cases and boundary conditions."""

    def test_divide_very_large_numbers(self, calculator):
        """Verify division works with very large numbers."""
        large_num = 10 ** 100
        assert calculator.divide(large_num, large_num) == 1
        assert calculator.divide(large_num, 2) == large_num / 2

    def test_divide_very_small_numbers(self, calculator):
        """Verify division works with very small floating-point numbers."""
        small_num = 1e-100
        result = calculator.divide(small_num, 2)
        assert result == pytest.approx(small_num / 2)

    def test_divide_infinity(self, calculator):
        """Verify division with infinity returns infinity or raises appropriate error."""
        inf = float('inf')
        # inf / 2 = inf
        assert calculator.divide(inf, 2) == inf
        # 10 / inf = 0
        assert calculator.divide(10, inf) == 0
        # inf / 0 raises ZeroDivisionError
        with pytest.raises(ZeroDivisionError):
            calculator.divide(inf, 0)

    def test_divide_negative_infinity(self, calculator):
        """Verify division with negative infinity."""
        neg_inf = float('-inf')
        assert calculator.divide(neg_inf, 2) == neg_inf
        assert calculator.divide(10, neg_inf) == 0

    def test_divide_nan(self, calculator):
        """Verify division with NaN."""
        nan = float('nan')
        result = calculator.divide(nan, 2)
        assert math.isnan(result)
        result2 = calculator.divide(10, nan)
        assert math.isnan(result2)

    def test_divide_mixed_int_float(self, calculator):
        """Verify division works with mixed int and float types."""
        assert calculator.divide(10, 3.0) == pytest.approx(10 / 3.0)
        assert calculator.divide(10.0, 3) == pytest.approx(10.0 / 3)

    def test_divide_complex_numbers(self, calculator):
        """Verify division with complex numbers."""
        result = calculator.divide(4 + 2j, 2)
        assert result == (4 + 2j) / 2
        assert result == (2 + 1j)

    def test_divide_one_by_large_number(self, calculator):
        """Verify dividing 1 by a very large number gives a very small result."""
        result = calculator.divide(1, 10 ** 100)
        assert result == pytest.approx(1e-100)

    def test_divide_preserves_precision(self, calculator):
        """Verify division maintains reasonable floating-point precision."""
        # Test with fractions that should have exact or near-exact representations
        assert calculator.divide(0.1, 0.1) == pytest.approx(1.0)
        assert calculator.divide(0.5, 0.2) == pytest.approx(2.5)