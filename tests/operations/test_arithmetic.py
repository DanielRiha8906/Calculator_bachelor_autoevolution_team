"""Tests for pure arithmetic functions from src.operations.arithmetic."""

import pytest
from src.operations.arithmetic import add, subtract, multiply, divide


class TestAddFunction:
    """Test the add pure function."""

    def test_add_positive_integers(self):
        """Test adding two positive integers."""
        assert add(2, 3) == 5

    def test_add_negative_integers(self):
        """Test adding two negative integers."""
        assert add(-2, -3) == -5

    def test_add_mixed_sign(self):
        """Test adding positive and negative."""
        assert add(5, -3) == 2

    def test_add_zero_left(self):
        """Test adding with zero on left."""
        assert add(0, 5) == 5

    def test_add_zero_right(self):
        """Test adding with zero on right."""
        assert add(5, 0) == 5

    def test_add_both_zeros(self):
        """Test adding two zeros."""
        assert add(0, 0) == 0

    def test_add_floats(self):
        """Test adding floats."""
        assert add(1.5, 2.5) == 4.0

    def test_add_float_negative(self):
        """Test adding negative floats."""
        assert add(-1.5, -2.5) == -4.0

    def test_add_mixed_int_float(self):
        """Test adding integer and float."""
        assert add(2, 3.5) == 5.5

    def test_add_very_large_numbers(self):
        """Test adding very large numbers."""
        assert add(1e10, 1e10) == 2e10

    def test_add_very_small_floats(self):
        """Test adding very small floats."""
        result = add(1e-10, 2e-10)
        assert abs(result - 3e-10) < 1e-15


class TestSubtractFunction:
    """Test the subtract pure function."""

    def test_subtract_positive_integers(self):
        """Test subtracting two positive integers."""
        assert subtract(5, 3) == 2

    def test_subtract_result_zero(self):
        """Test subtraction resulting in zero."""
        assert subtract(5, 5) == 0

    def test_subtract_result_negative(self):
        """Test subtraction resulting in negative."""
        assert subtract(3, 5) == -2

    def test_subtract_negative_integers(self):
        """Test subtracting negative integers."""
        assert subtract(-2, -3) == 1

    def test_subtract_negative_from_positive(self):
        """Test subtracting negative from positive."""
        assert subtract(5, -3) == 8

    def test_subtract_positive_from_negative(self):
        """Test subtracting positive from negative."""
        assert subtract(-5, 3) == -8

    def test_subtract_zero_left(self):
        """Test subtracting with zero on left."""
        assert subtract(0, 5) == -5

    def test_subtract_zero_right(self):
        """Test subtracting with zero on right."""
        assert subtract(5, 0) == 5

    def test_subtract_both_zeros(self):
        """Test subtracting two zeros."""
        assert subtract(0, 0) == 0

    def test_subtract_floats(self):
        """Test subtracting floats."""
        assert subtract(5.5, 2.5) == 3.0

    def test_subtract_float_negative(self):
        """Test subtracting negative floats."""
        assert subtract(-5.5, -2.5) == -3.0

    def test_subtract_mixed_int_float(self):
        """Test subtracting integer and float."""
        assert subtract(5, 2.5) == 2.5

    def test_subtract_very_large_numbers(self):
        """Test subtracting very large numbers."""
        assert subtract(1e10, 5e9) == 5e9


class TestMultiplyFunction:
    """Test the multiply pure function."""

    def test_multiply_positive_integers(self):
        """Test multiplying two positive integers."""
        assert multiply(3, 4) == 12

    def test_multiply_by_zero_left(self):
        """Test multiplying with zero on left."""
        assert multiply(0, 5) == 0

    def test_multiply_by_zero_right(self):
        """Test multiplying with zero on right."""
        assert multiply(5, 0) == 0

    def test_multiply_both_zeros(self):
        """Test multiplying two zeros."""
        assert multiply(0, 0) == 0

    def test_multiply_by_one_left(self):
        """Test multiplying with one on left."""
        assert multiply(1, 5) == 5

    def test_multiply_by_one_right(self):
        """Test multiplying with one on right."""
        assert multiply(5, 1) == 5

    def test_multiply_negative_integers(self):
        """Test multiplying two negative integers."""
        assert multiply(-3, -4) == 12

    def test_multiply_negative_positive(self):
        """Test multiplying negative and positive."""
        assert multiply(-3, 4) == -12

    def test_multiply_floats(self):
        """Test multiplying floats."""
        assert multiply(2.5, 4.0) == 10.0

    def test_multiply_float_negative(self):
        """Test multiplying negative floats."""
        assert multiply(-2.5, -4.0) == 10.0

    def test_multiply_mixed_int_float(self):
        """Test multiplying integer and float."""
        assert multiply(3, 2.5) == 7.5

    def test_multiply_fraction_result(self):
        """Test multiplication resulting in fraction."""
        assert multiply(0.5, 0.5) == 0.25

    def test_multiply_very_large_numbers(self):
        """Test multiplying very large numbers."""
        assert multiply(1e10, 2e10) == 2e20

    def test_multiply_result_one(self):
        """Test multiplication resulting in one."""
        assert multiply(2, 0.5) == 1.0


class TestDivideFunction:
    """Test the divide pure function."""

    def test_divide_positive_integers(self):
        """Test dividing two positive integers."""
        assert divide(6, 3) == 2.0

    def test_divide_normal(self):
        """Test normal division."""
        assert divide(10, 2) == 5.0

    def test_divide_by_zero_raises_error(self):
        """Test that dividing by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            divide(5, 0)

    def test_divide_by_zero_zero_numerator(self):
        """Test that 0/0 raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            divide(0, 0)

    def test_divide_zero_numerator(self):
        """Test dividing zero by non-zero."""
        assert divide(0, 5) == 0.0

    def test_divide_negative_integers(self):
        """Test dividing two negative integers."""
        assert divide(-6, -3) == 2.0

    def test_divide_negative_positive(self):
        """Test dividing negative by positive."""
        assert divide(-6, 3) == -2.0

    def test_divide_positive_negative(self):
        """Test dividing positive by negative."""
        assert divide(6, -3) == -2.0

    def test_divide_floats(self):
        """Test dividing floats."""
        assert divide(5.0, 2.0) == 2.5

    def test_divide_float_negative(self):
        """Test dividing negative floats."""
        assert divide(-5.0, -2.0) == 2.5

    def test_divide_mixed_int_float(self):
        """Test dividing integer by float."""
        assert divide(5, 2.0) == 2.5

    def test_divide_fractional_result(self):
        """Test division with fractional result."""
        assert divide(1, 3) == pytest.approx(0.3333333, rel=1e-5)

    def test_divide_result_less_than_one(self):
        """Test division resulting in less than one."""
        assert divide(1, 2) == 0.5

    def test_divide_very_large_by_small(self):
        """Test dividing very large by very small."""
        result = divide(1e10, 1e-5)
        assert result == pytest.approx(1e15)

    def test_divide_very_small_by_large(self):
        """Test dividing very small by very large."""
        result = divide(1e-10, 1e5)
        assert result == pytest.approx(1e-15)

    def test_divide_one_by_one(self):
        """Test dividing one by one."""
        assert divide(1, 1) == 1.0

    def test_divide_negative_zero_numerator(self):
        """Test dividing negative zero."""
        assert divide(-0.0, 5) == 0.0


class TestArithmeticEdgeCases:
    """Test edge cases for arithmetic functions."""

    def test_add_commutative(self):
        """Test that addition is commutative."""
        assert add(3, 5) == add(5, 3)

    def test_subtract_non_commutative(self):
        """Test that subtraction is not commutative."""
        assert subtract(5, 3) != subtract(3, 5)

    def test_multiply_commutative(self):
        """Test that multiplication is commutative."""
        assert multiply(3, 5) == multiply(5, 3)

    def test_divide_non_commutative(self):
        """Test that division is not commutative."""
        assert divide(6, 3) != divide(3, 6)

    def test_operations_with_infinity(self):
        """Test operations with infinity."""
        inf = float('inf')
        assert add(inf, 1) == inf
        assert multiply(inf, 2) == inf
        with pytest.raises(ZeroDivisionError):
            divide(inf, 0)

    def test_add_with_nan(self):
        """Test add with NaN."""
        nan = float('nan')
        result = add(nan, 1)
        assert result != result  # NaN != NaN

    def test_chained_operations(self):
        """Test chaining multiple operations."""
        result = add(2, 3)  # 5
        result = multiply(result, 2)  # 10
        result = subtract(result, 5)  # 5
        assert result == 5

    def test_very_precise_float_division(self):
        """Test division with precise floats."""
        result = divide(1, 3)
        # Should be approximately 0.333...
        assert abs(result * 3 - 1.0) < 1e-10
