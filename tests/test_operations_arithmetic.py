"""Comprehensive tests for arithmetic operations module.

Tests cover all four basic arithmetic functions (add, subtract, multiply, divide)
with normal cases, edge cases, and error conditions.
"""

import pytest
import math
from src.operations import arithmetic


class TestAdd:
    """Test suite for arithmetic.add()"""

    def test_add_positive_integers(self):
        """Happy path: adding two positive integers."""
        assert arithmetic.add(2, 3) == 5

    def test_add_positive_floats(self):
        """Happy path: adding two positive floats."""
        result = arithmetic.add(2.5, 3.5)
        assert abs(result - 6.0) < 1e-10

    def test_add_negative_integers(self):
        """Adding negative integers."""
        assert arithmetic.add(-2, -3) == -5

    def test_add_mixed_signs(self):
        """Adding positive and negative numbers."""
        assert arithmetic.add(10, -3) == 7

    def test_add_zero_to_number(self):
        """Adding zero should return the same number."""
        assert arithmetic.add(42, 0) == 42
        assert arithmetic.add(0, 42) == 42

    def test_add_two_zeros(self):
        """Adding zero to zero."""
        assert arithmetic.add(0, 0) == 0

    def test_add_large_numbers(self):
        """Adding very large numbers."""
        large = 10**100
        assert arithmetic.add(large, large) == 2 * large

    def test_add_very_small_floats(self):
        """Adding very small floating-point numbers."""
        small = 1e-15
        result = arithmetic.add(small, small)
        assert abs(result - 2e-15) < 1e-20

    def test_add_negative_float_to_positive(self):
        """Adding negative float to positive."""
        result = arithmetic.add(5.5, -2.5)
        assert abs(result - 3.0) < 1e-10

    def test_add_commutative(self):
        """Addition is commutative: a + b == b + a."""
        a, b = 7.3, 4.2
        assert arithmetic.add(a, b) == arithmetic.add(b, a)

    def test_add_infinity(self):
        """Adding infinity."""
        result = arithmetic.add(float('inf'), 100)
        assert result == float('inf')

    def test_add_infinity_negative(self):
        """Adding negative infinity."""
        result = arithmetic.add(float('-inf'), 100)
        assert result == float('-inf')

    def test_add_two_infinities(self):
        """Adding positive and negative infinities results in NaN."""
        result = arithmetic.add(float('inf'), float('-inf'))
        assert math.isnan(result)

    def test_add_nan_propagates(self):
        """Adding NaN to any number results in NaN."""
        result = arithmetic.add(float('nan'), 10)
        assert math.isnan(result)

    def test_add_string_concatenates(self):
        """Python allows string addition (concatenation)."""
        # Note: The function accepts strings even though type hints say float
        result = arithmetic.add("hello", "world")
        assert result == "helloworld"

    def test_add_string_and_int_raises_error(self):
        """Adding string and int should raise TypeError."""
        with pytest.raises(TypeError):
            arithmetic.add("5", 3)

    def test_add_none_raises_error(self):
        """Adding None should raise TypeError."""
        with pytest.raises(TypeError):
            arithmetic.add(None, 5)


class TestSubtract:
    """Test suite for arithmetic.subtract()"""

    def test_subtract_positive_integers(self):
        """Happy path: subtracting two positive integers."""
        assert arithmetic.subtract(5, 3) == 2

    def test_subtract_positive_floats(self):
        """Happy path: subtracting two positive floats."""
        result = arithmetic.subtract(5.5, 2.5)
        assert abs(result - 3.0) < 1e-10

    def test_subtract_negative_integers(self):
        """Subtracting negative integers (double negative)."""
        assert arithmetic.subtract(-2, -3) == 1

    def test_subtract_negative_from_positive(self):
        """Subtracting negative from positive adds the magnitude."""
        assert arithmetic.subtract(10, -5) == 15

    def test_subtract_positive_from_negative(self):
        """Subtracting positive from negative."""
        assert arithmetic.subtract(-10, 5) == -15

    def test_subtract_zero(self):
        """Subtracting zero should return the same number."""
        assert arithmetic.subtract(42, 0) == 42

    def test_subtract_from_zero(self):
        """Subtracting from zero."""
        assert arithmetic.subtract(0, 42) == -42

    def test_subtract_equal_values(self):
        """Subtracting a number from itself returns zero."""
        assert arithmetic.subtract(7, 7) == 0

    def test_subtract_large_numbers(self):
        """Subtracting very large numbers."""
        large = 10**100
        assert arithmetic.subtract(large * 2, large) == large

    def test_subtract_very_small_floats(self):
        """Subtracting very small floating-point numbers."""
        small = 1e-15
        result = arithmetic.subtract(3 * small, small)
        assert abs(result - 2e-15) < 1e-20

    def test_subtract_infinity(self):
        """Subtracting from infinity."""
        result = arithmetic.subtract(float('inf'), 100)
        assert result == float('inf')

    def test_subtract_infinity_from_number(self):
        """Subtracting infinity from a number."""
        result = arithmetic.subtract(100, float('inf'))
        assert result == float('-inf')

    def test_subtract_infinities(self):
        """Subtracting equal infinities results in NaN."""
        result = arithmetic.subtract(float('inf'), float('inf'))
        assert math.isnan(result)

    def test_subtract_nan_propagates(self):
        """Subtracting NaN results in NaN."""
        result = arithmetic.subtract(float('nan'), 10)
        assert math.isnan(result)

    def test_subtract_string_raises_error(self):
        """Subtracting strings should raise TypeError."""
        with pytest.raises(TypeError):
            arithmetic.subtract("hello", "world")

    def test_subtract_none_raises_error(self):
        """Subtracting None should raise TypeError."""
        with pytest.raises(TypeError):
            arithmetic.subtract(None, 5)

    def test_subtract_is_not_commutative(self):
        """Subtraction is not commutative: a - b != b - a (usually)."""
        a, b = 10, 3
        assert arithmetic.subtract(a, b) != arithmetic.subtract(b, a)
        assert arithmetic.subtract(a, b) == 7
        assert arithmetic.subtract(b, a) == -7


class TestMultiply:
    """Test suite for arithmetic.multiply()"""

    def test_multiply_positive_integers(self):
        """Happy path: multiplying two positive integers."""
        assert arithmetic.multiply(3, 4) == 12

    def test_multiply_positive_floats(self):
        """Happy path: multiplying two positive floats."""
        result = arithmetic.multiply(2.5, 4.0)
        assert abs(result - 10.0) < 1e-10

    def test_multiply_negative_integers(self):
        """Multiplying two negative integers (positive result)."""
        assert arithmetic.multiply(-3, -4) == 12

    def test_multiply_mixed_signs(self):
        """Multiplying numbers with opposite signs (negative result)."""
        assert arithmetic.multiply(3, -4) == -12
        assert arithmetic.multiply(-3, 4) == -12

    def test_multiply_by_zero(self):
        """Multiplying by zero always returns zero."""
        assert arithmetic.multiply(42, 0) == 0
        assert arithmetic.multiply(0, 42) == 0

    def test_multiply_by_one(self):
        """Multiplying by one returns the same number."""
        assert arithmetic.multiply(42, 1) == 42
        assert arithmetic.multiply(1, 42) == 42

    def test_multiply_zero_by_zero(self):
        """Multiplying zero by zero."""
        assert arithmetic.multiply(0, 0) == 0

    def test_multiply_by_negative_one(self):
        """Multiplying by -1 negates the number."""
        assert arithmetic.multiply(42, -1) == -42
        assert arithmetic.multiply(-1, 42) == -42

    def test_multiply_large_numbers(self):
        """Multiplying very large numbers."""
        large = 10**50
        result = arithmetic.multiply(large, 2)
        assert result == 2 * large

    def test_multiply_very_small_floats(self):
        """Multiplying very small floating-point numbers."""
        small = 1e-15
        result = arithmetic.multiply(small, small)
        assert abs(result - 1e-30) < 1e-40

    def test_multiply_commutative(self):
        """Multiplication is commutative: a * b == b * a."""
        a, b = 7.3, 4.2
        assert arithmetic.multiply(a, b) == arithmetic.multiply(b, a)

    def test_multiply_by_infinity(self):
        """Multiplying by infinity."""
        result = arithmetic.multiply(5, float('inf'))
        assert result == float('inf')

    def test_multiply_zero_by_infinity(self):
        """Multiplying zero by infinity results in NaN."""
        result = arithmetic.multiply(0, float('inf'))
        assert math.isnan(result)

    def test_multiply_negative_by_infinity(self):
        """Multiplying negative number by infinity."""
        result = arithmetic.multiply(-5, float('inf'))
        assert result == float('-inf')

    def test_multiply_nan_propagates(self):
        """Multiplying by NaN results in NaN."""
        result = arithmetic.multiply(float('nan'), 10)
        assert math.isnan(result)

    def test_multiply_string_raises_error(self):
        """Multiplying strings (would concatenate in Python, but type-hinted as float)."""
        # Note: Python allows int * str (repetition), but not float * str
        with pytest.raises(TypeError):
            arithmetic.multiply(3.5, "hello")

    def test_multiply_none_raises_error(self):
        """Multiplying by None should raise TypeError."""
        with pytest.raises(TypeError):
            arithmetic.multiply(None, 5)


class TestDivide:
    """Test suite for arithmetic.divide()"""

    def test_divide_positive_integers(self):
        """Happy path: dividing two positive integers."""
        assert arithmetic.divide(12, 3) == 4.0

    def test_divide_positive_floats(self):
        """Happy path: dividing two positive floats."""
        result = arithmetic.divide(10.0, 2.5)
        assert abs(result - 4.0) < 1e-10

    def test_divide_negative_integers(self):
        """Dividing two negative integers (positive result)."""
        assert arithmetic.divide(-12, -3) == 4.0

    def test_divide_mixed_signs(self):
        """Dividing numbers with opposite signs (negative result)."""
        assert arithmetic.divide(12, -3) == -4.0
        assert arithmetic.divide(-12, 3) == -4.0

    def test_divide_zero_dividend(self):
        """Dividing zero by a nonzero number returns zero."""
        assert arithmetic.divide(0, 5) == 0.0

    def test_divide_by_zero_raises_error(self):
        """Dividing by zero raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            arithmetic.divide(10, 0)
        assert str(exc_info.value) == "Division by zero is not allowed"

    def test_divide_zero_by_zero_raises_error(self):
        """Dividing zero by zero raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            arithmetic.divide(0, 0)
        assert str(exc_info.value) == "Division by zero is not allowed"

    def test_divide_by_one(self):
        """Dividing by one returns the same number."""
        assert arithmetic.divide(42, 1) == 42.0

    def test_divide_by_negative_one(self):
        """Dividing by -1 negates the number."""
        assert arithmetic.divide(42, -1) == -42.0

    def test_divide_one_by_number(self):
        """Dividing one by a number gives reciprocal."""
        result = arithmetic.divide(1, 2)
        assert abs(result - 0.5) < 1e-10

    def test_divide_creates_fraction(self):
        """Dividing integers that don't divide evenly creates float."""
        result = arithmetic.divide(1, 3)
        assert abs(result - 1/3) < 1e-10

    def test_divide_large_by_small(self):
        """Dividing large number by small number."""
        result = arithmetic.divide(10**100, 10**-50)
        # Use approximate comparison due to floating point precision
        assert result == pytest.approx(10**150)

    def test_divide_very_small_floats(self):
        """Dividing very small floating-point numbers."""
        small = 1e-15
        result = arithmetic.divide(small, 2)
        assert abs(result - 5e-16) < 1e-25

    def test_divide_by_very_small_nonzero(self):
        """Dividing by very small nonzero number produces large result."""
        result = arithmetic.divide(1, 1e-15)
        assert result == pytest.approx(1e15)

    def test_divide_infinity_by_nonzero(self):
        """Dividing infinity by a nonzero number."""
        result = arithmetic.divide(float('inf'), 2)
        assert result == float('inf')

    def test_divide_nonzero_by_infinity(self):
        """Dividing a nonzero number by infinity."""
        result = arithmetic.divide(5, float('inf'))
        assert result == 0.0

    def test_divide_infinity_by_infinity(self):
        """Dividing infinity by infinity results in NaN."""
        result = arithmetic.divide(float('inf'), float('inf'))
        assert math.isnan(result)

    def test_divide_nan_propagates(self):
        """Dividing by or NaN results in NaN."""
        result = arithmetic.divide(float('nan'), 10)
        assert math.isnan(result)

    def test_divide_by_nan_raises_comparison(self):
        """Dividing by NaN - NaN doesn't equal 0 in comparison."""
        # NaN != 0, so it won't trigger the zero check
        result = arithmetic.divide(10, float('nan'))
        assert math.isnan(result)

    def test_divide_string_raises_error(self):
        """Dividing strings should raise TypeError."""
        with pytest.raises(TypeError):
            arithmetic.divide("hello", "world")

    def test_divide_none_raises_error(self):
        """Dividing by None should raise TypeError."""
        with pytest.raises(TypeError):
            arithmetic.divide(None, 5)

    def test_divide_by_negative_zero(self):
        """Dividing by negative zero (which is technically zero)."""
        with pytest.raises(ValueError) as exc_info:
            arithmetic.divide(10, -0.0)
        assert str(exc_info.value) == "Division by zero is not allowed"

    def test_divide_result_type(self):
        """Division always returns a float."""
        result = arithmetic.divide(10, 2)
        assert isinstance(result, float)


class TestArithmeticIntegration:
    """Integration tests combining multiple arithmetic operations."""

    def test_associative_property_addition(self):
        """(a + b) + c == a + (b + c)."""
        a, b, c = 5, 3, 2
        left = arithmetic.add(arithmetic.add(a, b), c)
        right = arithmetic.add(a, arithmetic.add(b, c))
        assert left == right

    def test_associative_property_multiplication(self):
        """(a * b) * c == a * (b * c)."""
        a, b, c = 5, 3, 2
        left = arithmetic.multiply(arithmetic.multiply(a, b), c)
        right = arithmetic.multiply(a, arithmetic.multiply(b, c))
        assert left == right

    def test_distributive_property(self):
        """a * (b + c) == (a * b) + (a * c)."""
        a, b, c = 5, 3, 2
        left = arithmetic.multiply(a, arithmetic.add(b, c))
        right = arithmetic.add(
            arithmetic.multiply(a, b),
            arithmetic.multiply(a, c)
        )
        assert abs(left - right) < 1e-10

    def test_subtract_is_add_negation(self):
        """a - b == a + (-b)."""
        a, b = 10, 3
        result1 = arithmetic.subtract(a, b)
        result2 = arithmetic.add(a, -b)
        assert result1 == result2

    def test_divide_is_multiply_inverse(self):
        """a / b == a * (1/b)."""
        a, b = 20, 4
        result1 = arithmetic.divide(a, b)
        result2 = arithmetic.multiply(a, arithmetic.divide(1, b))
        assert abs(result1 - result2) < 1e-10
