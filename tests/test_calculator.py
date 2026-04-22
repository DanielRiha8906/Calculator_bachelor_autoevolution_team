import pytest
import math
from src.calculator import Calculator


@pytest.fixture
def calc():
    """Fixture providing a Calculator instance for tests."""
    return Calculator()


class TestDivision:
    """Tests for the divide method with valid and invalid inputs."""

    def test_divide_positive_numbers(self, calc):
        """Test division with positive integers."""
        assert calc.divide(10, 2) == 5

    def test_divide_with_floats(self, calc):
        """Test division with floating point numbers."""
        assert calc.divide(7.5, 2.5) == 3.0

    def test_divide_negative_numbers(self, calc):
        """Test division with negative numbers."""
        assert calc.divide(-10, 2) == -5
        assert calc.divide(10, -2) == -5

    def test_divide_by_zero_raises_exception(self, calc):
        """Test that division by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calc.divide(10, 0)

    def test_divide_zero_by_nonzero(self, calc):
        """Test dividing zero by a nonzero number returns zero."""
        assert calc.divide(0, 5) == 0

    @pytest.mark.parametrize("invalid_a,invalid_b", [
        ("10", 2),       # string as dividend
        (10, "2"),       # string as divisor
        (None, 5),       # None as dividend
        (5, None),       # None as divisor
        ([10], 2),       # list as dividend
        (10, [2]),       # list as divisor
    ])
    def test_divide_non_numeric_inputs_raise_typeerror(self, calc, invalid_a, invalid_b):
        """Test that non-numeric inputs (string, None, list) raise TypeError."""
        with pytest.raises(TypeError):
            calc.divide(invalid_a, invalid_b)

    def test_divide_result_precision(self, calc):
        """Test division result with expected precision."""
        result = calc.divide(10, 3)
        assert abs(result - 3.333333333333333) < 1e-10

    def test_divide_large_numbers(self, calc):
        """Test division with very large numbers."""
        assert calc.divide(10**15, 10**10) == 10**5

    def test_divide_very_small_numbers(self, calc):
        """Test division with very small numbers."""
        result = calc.divide(1e-10, 1e-5)
        assert abs(result - 1e-5) < 1e-15