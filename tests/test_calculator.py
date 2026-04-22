import pytest
import math
from src.calculator import Calculator


class TestDivide:
    """Test suite for Calculator.divide() method."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance for each test."""
        return Calculator()

    # Happy Path Tests
    def test_divide_positive_numbers(self, calculator):
        """Test division of two positive numbers returns correct result."""
        result = calculator.divide(10, 2)
        assert result == 5.0

    def test_divide_negative_numerator(self, calculator):
        """Test division with negative numerator."""
        result = calculator.divide(-10, 2)
        assert result == -5.0

    def test_divide_negative_denominator(self, calculator):
        """Test division with negative denominator."""
        result = calculator.divide(10, -2)
        assert result == -5.0

    def test_divide_both_negative(self, calculator):
        """Test division with both negative numbers."""
        result = calculator.divide(-10, -2)
        assert result == 5.0

    def test_divide_fractional_result(self, calculator):
        """Test division that produces a fractional result."""
        result = calculator.divide(7, 2)
        assert result == 3.5

    def test_divide_zero_numerator(self, calculator):
        """Test division with zero numerator returns 0.0 without error."""
        result = calculator.divide(0, 5)
        assert result == 0.0

    def test_divide_zero_numerator_with_float_denominator(self, calculator):
        """Test division with zero numerator and float denominator."""
        result = calculator.divide(0, 2.5)
        assert result == 0.0

    def test_divide_floating_point_numbers(self, calculator):
        """Test division of floating point numbers."""
        result = calculator.divide(7.5, 2.5)
        assert result == 3.0

    # Edge Cases: Division by Zero
    @pytest.mark.parametrize("numerator", [0, 1, -1, 10, -10, 3.14, -2.71])
    def test_divide_by_zero_integer(self, calculator, numerator):
        """Test division by zero (integer) raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(numerator, 0)

    @pytest.mark.parametrize("numerator", [0, 1, -1, 10, -10, 3.14, -2.71])
    def test_divide_by_zero_float(self, calculator, numerator):
        """Test division by zero (float 0.0) raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(numerator, 0.0)

    # Edge Cases: Very Large and Very Small Numbers
    def test_divide_very_large_numbers(self, calculator):
        """Test division with very large numbers."""
        result = calculator.divide(1e100, 1e50)
        assert abs(result - 1e50) < 1e35

    def test_divide_very_small_numbers(self, calculator):
        """Test division with very small numbers."""
        result = calculator.divide(1e-100, 1e-50)
        assert result == 1e-50

    def test_divide_results_in_very_small_number(self, calculator):
        """Test division that results in a very small number."""
        result = calculator.divide(1e-100, 1e50)
        assert result == 1e-150

    # Edge Cases: Type Handling
    def test_divide_mixed_int_float(self, calculator):
        """Test division with mixed integer and float types."""
        result = calculator.divide(5, 2.0)
        assert result == 2.5

    def test_divide_float_numerator_int_denominator(self, calculator):
        """Test division with float numerator and int denominator."""
        result = calculator.divide(5.0, 2)
        assert result == 2.5

    # Edge Cases: Result Precision
    def test_divide_result_precision(self, calculator):
        """Test division precision with repeating decimal."""
        result = calculator.divide(1, 3)
        assert abs(result - 0.3333333333333333) < 1e-15