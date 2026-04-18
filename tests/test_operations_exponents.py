"""Comprehensive tests for exponent operations module.

Tests cover power, factorial, square, and cube operations with normal cases,
edge cases, and error conditions.
"""

import pytest
import math
from src.operations import exponents


class TestPower:
    """Test suite for exponents.power()"""

    def test_power_positive_base_positive_exponent(self):
        """Happy path: positive base raised to positive exponent."""
        assert exponents.power(2, 3) == 8
        assert exponents.power(3, 2) == 9

    def test_power_positive_base_zero_exponent(self):
        """Any positive base to the power of 0 equals 1."""
        assert exponents.power(5, 0) == 1
        assert exponents.power(100, 0) == 1

    def test_power_zero_base_positive_exponent(self):
        """Zero raised to any positive exponent is 0."""
        assert exponents.power(0, 5) == 0
        assert exponents.power(0, 100) == 0

    def test_power_zero_base_zero_exponent(self):
        """0^0 is mathematically undefined but Python evaluates to 1."""
        assert exponents.power(0, 0) == 1

    def test_power_one_any_exponent(self):
        """1 raised to any exponent is 1."""
        assert exponents.power(1, 5) == 1
        assert exponents.power(1, -5) == 1
        assert exponents.power(1, 0) == 1

    def test_power_negative_base_even_exponent(self):
        """Negative base with even exponent gives positive result."""
        assert exponents.power(-2, 4) == 16
        assert exponents.power(-3, 2) == 9

    def test_power_negative_base_odd_exponent(self):
        """Negative base with odd exponent gives negative result."""
        assert exponents.power(-2, 3) == -8
        assert exponents.power(-3, 1) == -3

    def test_power_base_one_negative_exponent(self):
        """1 raised to negative exponent is 1."""
        assert exponents.power(1, -10) == 1

    def test_power_positive_base_negative_exponent(self):
        """Positive base with negative exponent gives reciprocal."""
        result = exponents.power(2, -1)
        assert abs(result - 0.5) < 1e-10

    def test_power_fractional_exponent(self):
        """Fractional exponent (square root)."""
        result = exponents.power(4, 0.5)
        assert abs(result - 2.0) < 1e-10

    def test_power_fractional_exponent_cube_root(self):
        """Fractional exponent (cube root)."""
        result = exponents.power(8, 1/3)
        assert abs(result - 2.0) < 1e-10

    def test_power_negative_base_fractional_exponent(self):
        """Negative base with fractional exponent can produce complex result."""
        # Python's ** operator returns complex for negative base and fractional exponent
        result = exponents.power(-4, 0.5)
        # math.isnan() expects a float, not complex, so we skip that check
        assert isinstance(result, complex)

    def test_power_large_numbers(self):
        """Large base and exponent."""
        result = exponents.power(10, 10)
        assert result == 10**10

    def test_power_float_base_float_exponent(self):
        """Floating-point base and exponent."""
        result = exponents.power(2.5, 2.0)
        assert abs(result - 6.25) < 1e-10

    def test_power_very_small_exponent(self):
        """Very small positive exponent (approaching 0)."""
        result = exponents.power(2, 0.0001)
        assert 0.99 < result < 1.01  # Should be close to 1

    def test_power_large_negative_exponent(self):
        """Large negative exponent gives very small result."""
        result = exponents.power(2, -20)
        assert result == pytest.approx(1 / (2**20))

    def test_power_infinity_exponent(self):
        """Infinity as exponent."""
        result = exponents.power(2, float('inf'))
        assert result == float('inf')

    def test_power_negative_infinity_exponent(self):
        """Negative infinity as exponent."""
        result = exponents.power(2, float('-inf'))
        assert result == 0.0

    def test_power_infinity_base(self):
        """Infinity as base."""
        result = exponents.power(float('inf'), 2)
        assert result == float('inf')

    def test_power_nan_propagates(self):
        """NaN in base or exponent produces NaN."""
        result = exponents.power(float('nan'), 2)
        assert math.isnan(result)

    def test_power_string_base_raises_error(self):
        """String as base should raise TypeError."""
        with pytest.raises(TypeError):
            exponents.power("2", 3)

    def test_power_string_exponent_raises_error(self):
        """String as exponent should raise TypeError."""
        with pytest.raises(TypeError):
            exponents.power(2, "3")

    def test_power_none_raises_error(self):
        """None as base or exponent should raise TypeError."""
        with pytest.raises(TypeError):
            exponents.power(None, 3)


class TestFactorial:
    """Test suite for exponents.factorial()"""

    def test_factorial_zero(self):
        """0! = 1."""
        assert exponents.factorial(0) == 1

    def test_factorial_one(self):
        """1! = 1."""
        assert exponents.factorial(1) == 1

    def test_factorial_small_positive(self):
        """Happy path: factorials of small positive integers."""
        assert exponents.factorial(2) == 2
        assert exponents.factorial(3) == 6
        assert exponents.factorial(5) == 120
        assert exponents.factorial(10) == 3628800

    def test_factorial_large_positive(self):
        """Factorial of larger integers."""
        assert exponents.factorial(20) == 2432902008176640000

    def test_factorial_negative_raises_error(self):
        """Negative integer factorial should raise ValueError."""
        with pytest.raises(ValueError) as exc_info:
            exponents.factorial(-1)
        assert "must be a non-negative integer" in str(exc_info.value)
        assert "-1" in str(exc_info.value)

    def test_factorial_large_negative_raises_error(self):
        """Large negative factorial should raise ValueError."""
        with pytest.raises(ValueError) as exc_info:
            exponents.factorial(-100)
        assert "must be a non-negative integer" in str(exc_info.value)

    def test_factorial_float_raises_error(self):
        """Float input should raise ValueError."""
        with pytest.raises(ValueError) as exc_info:
            exponents.factorial(5.0)
        assert "n must be an integer" in str(exc_info.value)
        assert "float" in str(exc_info.value)

    def test_factorial_string_raises_error(self):
        """String input should raise ValueError."""
        with pytest.raises(ValueError) as exc_info:
            exponents.factorial("5")
        assert "n must be an integer" in str(exc_info.value)

    def test_factorial_none_raises_error(self):
        """None input should raise ValueError."""
        with pytest.raises(ValueError) as exc_info:
            exponents.factorial(None)
        assert "n must be an integer" in str(exc_info.value)

    def test_factorial_list_raises_error(self):
        """List input should raise ValueError."""
        with pytest.raises(ValueError) as exc_info:
            exponents.factorial([5])
        assert "n must be an integer" in str(exc_info.value)

    def test_factorial_bool_is_int(self):
        """In Python, bool is an instance of int."""
        # True == 1, False == 0
        assert exponents.factorial(True) == 1
        assert exponents.factorial(False) == 1

    def test_factorial_very_large(self):
        """Factorial of very large integer (still reasonable)."""
        result = exponents.factorial(100)
        assert result > 0
        # 100! is approximately 9.33e157
        assert result > 1e150

    def test_factorial_negative_float_raises_error(self):
        """Negative float should raise ValueError (isinstance check first)."""
        with pytest.raises(ValueError) as exc_info:
            exponents.factorial(-5.5)
        # The isinstance check should catch this first
        assert "n must be an integer" in str(exc_info.value)

    def test_factorial_positive_bool_true(self):
        """Boolean True treated as integer 1."""
        assert exponents.factorial(True) == 1

    def test_factorial_positive_bool_false(self):
        """Boolean False treated as integer 0."""
        assert exponents.factorial(False) == 1


class TestSquare:
    """Test suite for exponents.square()"""

    def test_square_positive_integer(self):
        """Happy path: squaring positive integer."""
        assert exponents.square(3) == 9
        assert exponents.square(5) == 25

    def test_square_negative_integer(self):
        """Squaring negative integer gives positive result."""
        assert exponents.square(-3) == 9
        assert exponents.square(-5) == 25

    def test_square_zero(self):
        """Square of zero is zero."""
        assert exponents.square(0) == 0

    def test_square_one(self):
        """Square of one is one."""
        assert exponents.square(1) == 1

    def test_square_negative_one(self):
        """Square of negative one is one."""
        assert exponents.square(-1) == 1

    def test_square_positive_float(self):
        """Squaring positive float."""
        result = exponents.square(2.5)
        assert abs(result - 6.25) < 1e-10

    def test_square_negative_float(self):
        """Squaring negative float."""
        result = exponents.square(-3.5)
        assert abs(result - 12.25) < 1e-10

    def test_square_very_small_number(self):
        """Squaring very small number produces even smaller."""
        small = 1e-10
        result = exponents.square(small)
        assert abs(result - 1e-20) < 1e-30

    def test_square_large_number(self):
        """Squaring large number."""
        large = 10**50
        result = exponents.square(large)
        assert result == large**2

    def test_square_fraction(self):
        """Squaring fraction less than 1 gives smaller result."""
        result = exponents.square(0.5)
        assert abs(result - 0.25) < 1e-10

    def test_square_infinity(self):
        """Squaring infinity."""
        result = exponents.square(float('inf'))
        assert result == float('inf')

    def test_square_negative_infinity(self):
        """Squaring negative infinity."""
        result = exponents.square(float('-inf'))
        assert result == float('inf')

    def test_square_nan_propagates(self):
        """Squaring NaN."""
        result = exponents.square(float('nan'))
        assert math.isnan(result)

    def test_square_string_raises_error(self):
        """String input should raise TypeError."""
        with pytest.raises(TypeError):
            exponents.square("5")

    def test_square_none_raises_error(self):
        """None input should raise TypeError."""
        with pytest.raises(TypeError):
            exponents.square(None)

    def test_square_result_always_non_negative(self):
        """Result of square is always non-negative (or NaN/inf)."""
        assert exponents.square(7) >= 0
        assert exponents.square(-7) >= 0
        assert exponents.square(0) >= 0


class TestCube:
    """Test suite for exponents.cube()"""

    def test_cube_positive_integer(self):
        """Happy path: cubing positive integer."""
        assert exponents.cube(2) == 8
        assert exponents.cube(3) == 27

    def test_cube_negative_integer(self):
        """Cubing negative integer gives negative result."""
        assert exponents.cube(-2) == -8
        assert exponents.cube(-3) == -27

    def test_cube_zero(self):
        """Cube of zero is zero."""
        assert exponents.cube(0) == 0

    def test_cube_one(self):
        """Cube of one is one."""
        assert exponents.cube(1) == 1

    def test_cube_negative_one(self):
        """Cube of negative one is negative one."""
        assert exponents.cube(-1) == -1

    def test_cube_positive_float(self):
        """Cubing positive float."""
        result = exponents.cube(2.5)
        assert abs(result - 15.625) < 1e-10

    def test_cube_negative_float(self):
        """Cubing negative float."""
        result = exponents.cube(-2.5)
        assert abs(result - (-15.625)) < 1e-10

    def test_cube_very_small_number(self):
        """Cubing very small number."""
        small = 1e-10
        result = exponents.cube(small)
        assert abs(result - 1e-30) < 1e-40

    def test_cube_large_number(self):
        """Cubing large number."""
        large = 10**50
        result = exponents.cube(large)
        assert result == large**3

    def test_cube_fraction_less_than_one(self):
        """Cubing fraction less than 1."""
        result = exponents.cube(0.5)
        assert abs(result - 0.125) < 1e-10

    def test_cube_fraction_greater_than_one(self):
        """Cubing fraction greater than 1 but less than 10."""
        result = exponents.cube(2.0)
        assert abs(result - 8.0) < 1e-10

    def test_cube_infinity(self):
        """Cubing positive infinity."""
        result = exponents.cube(float('inf'))
        assert result == float('inf')

    def test_cube_negative_infinity(self):
        """Cubing negative infinity."""
        result = exponents.cube(float('-inf'))
        assert result == float('-inf')

    def test_cube_nan_propagates(self):
        """Cubing NaN."""
        result = exponents.cube(float('nan'))
        assert math.isnan(result)

    def test_cube_string_raises_error(self):
        """String input should raise TypeError."""
        with pytest.raises(TypeError):
            exponents.cube("5")

    def test_cube_none_raises_error(self):
        """None input should raise TypeError."""
        with pytest.raises(TypeError):
            exponents.cube(None)

    def test_cube_preserves_sign(self):
        """Cube preserves the sign of the input."""
        assert exponents.cube(5) > 0
        assert exponents.cube(-5) < 0
        assert exponents.cube(0) == 0


class TestExponentsIntegration:
    """Integration tests combining multiple exponent operations."""

    def test_square_equals_power_two(self):
        """square(x) should equal power(x, 2)."""
        x = 7
        assert exponents.square(x) == exponents.power(x, 2)

    def test_cube_equals_power_three(self):
        """cube(x) should equal power(x, 3)."""
        x = 4
        assert exponents.cube(x) == exponents.power(x, 3)

    def test_square_then_cube_equals_power_six(self):
        """(x^2)^3 = x^6."""
        x = 2
        result1 = exponents.cube(exponents.square(x))
        result2 = exponents.power(x, 6)
        assert result1 == result2

    def test_factorial_grows_faster_than_power(self):
        """Factorial grows much faster than power for large n."""
        n = 20
        factorial_result = exponents.factorial(n)
        power_result = exponents.power(n, n)
        assert factorial_result < power_result  # Usually true but not always

    def test_power_chain(self):
        """(a^b)^c = a^(b*c)."""
        a, b, c = 2, 3, 2
        left = exponents.power(exponents.power(a, b), c)
        right = exponents.power(a, b * c)
        assert left == right
