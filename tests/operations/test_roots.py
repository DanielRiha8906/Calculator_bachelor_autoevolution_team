"""Tests for root and exponentiation functions from src.operations.roots."""

import math
import pytest
from src.operations.roots import factorial, square, cube, square_root, cube_root


class TestFactorialFunction:
    """Test the factorial pure function."""

    def test_factorial_zero(self):
        """Test factorial of zero."""
        assert factorial(0) == 1

    def test_factorial_one(self):
        """Test factorial of one."""
        assert factorial(1) == 1

    def test_factorial_two(self):
        """Test factorial of two."""
        assert factorial(2) == 2

    def test_factorial_three(self):
        """Test factorial of three."""
        assert factorial(3) == 6

    def test_factorial_five(self):
        """Test factorial of five."""
        assert factorial(5) == 120

    def test_factorial_ten(self):
        """Test factorial of ten."""
        assert factorial(10) == 3628800

    def test_factorial_large_value(self):
        """Test factorial of large value."""
        assert factorial(20) == 2432902008176640000

    def test_factorial_result_is_int(self):
        """Test that factorial returns int."""
        result = factorial(5)
        assert isinstance(result, int)

    def test_factorial_float_integer_value(self):
        """Test factorial with float representing integer."""
        assert factorial(5.0) == 120

    def test_factorial_float_zero(self):
        """Test factorial with float zero."""
        assert factorial(0.0) == 1

    def test_factorial_negative_integer_raises_error(self):
        """Test that factorial of negative integer raises ValueError."""
        with pytest.raises(ValueError, match="not defined for negative values"):
            factorial(-1)

    def test_factorial_negative_one_raises_error(self):
        """Test that factorial of -1 raises ValueError."""
        with pytest.raises(ValueError, match="not defined for negative values"):
            factorial(-1)

    def test_factorial_float_non_integer_raises_error(self):
        """Test that factorial of non-integer float raises TypeError."""
        with pytest.raises(TypeError, match="only accepts integer values"):
            factorial(5.5)

    def test_factorial_negative_float_raises_error(self):
        """Test that factorial of negative float raises ValueError."""
        with pytest.raises(ValueError, match="not defined for negative values"):
            factorial(-1.0)

    def test_factorial_very_small_non_integer_raises_error(self):
        """Test that even small non-integer floats raise TypeError."""
        with pytest.raises(TypeError):
            factorial(5.0001)

    def test_factorial_negative_float_non_integer_raises_error(self):
        """Test that negative non-integer float raises appropriate error."""
        # Non-integer check happens before negative check for floats
        with pytest.raises(TypeError):
            factorial(-1.5)

    def test_factorial_growth(self):
        """Test factorial growth."""
        assert factorial(5) < factorial(6)
        assert factorial(6) < factorial(7)

    def test_factorial_properties(self):
        """Test factorial property: n! = n * (n-1)!"""
        for n in range(1, 10):
            assert factorial(n) == n * factorial(n - 1)


class TestSquareFunction:
    """Test the square pure function."""

    def test_square_positive_integer(self):
        """Test squaring positive integer."""
        assert square(5) == 25

    def test_square_zero(self):
        """Test squaring zero."""
        assert square(0) == 0

    def test_square_negative_integer(self):
        """Test squaring negative integer."""
        assert square(-5) == 25

    def test_square_positive_float(self):
        """Test squaring positive float."""
        assert square(2.5) == 6.25

    def test_square_negative_float(self):
        """Test squaring negative float."""
        assert square(-2.5) == 6.25

    def test_square_one(self):
        """Test squaring one."""
        assert square(1) == 1

    def test_square_large_value(self):
        """Test squaring large value."""
        assert square(1e5) == 1e10

    def test_square_small_float(self):
        """Test squaring small float."""
        result = square(0.1)
        assert result == pytest.approx(0.01)

    def test_square_result_always_non_negative(self):
        """Test that square is always non-negative."""
        values = [-10, -1, 0, 1, 10, 0.5, -0.5]
        for val in values:
            assert square(val) >= 0


class TestCubeFunction:
    """Test the cube pure function."""

    def test_cube_positive_integer(self):
        """Test cubing positive integer."""
        assert cube(2) == 8

    def test_cube_zero(self):
        """Test cubing zero."""
        assert cube(0) == 0

    def test_cube_negative_integer(self):
        """Test cubing negative integer."""
        assert cube(-2) == -8

    def test_cube_positive_float(self):
        """Test cubing positive float."""
        assert cube(1.5) == pytest.approx(3.375)

    def test_cube_negative_float(self):
        """Test cubing negative float."""
        assert cube(-1.5) == pytest.approx(-3.375)

    def test_cube_one(self):
        """Test cubing one."""
        assert cube(1) == 1

    def test_cube_negative_one(self):
        """Test cubing negative one."""
        assert cube(-1) == -1

    def test_cube_large_value(self):
        """Test cubing large value."""
        assert cube(1e5) == 1e15

    def test_cube_small_float(self):
        """Test cubing small float."""
        result = cube(0.1)
        assert result == pytest.approx(0.001)

    def test_cube_preserves_sign(self):
        """Test that cube preserves sign."""
        assert cube(5) > 0
        assert cube(-5) < 0
        assert cube(0) == 0


class TestSquareRootFunction:
    """Test the square_root pure function."""

    def test_square_root_perfect_square(self):
        """Test square root of perfect square."""
        assert square_root(16) == 4.0

    def test_square_root_zero(self):
        """Test square root of zero."""
        assert square_root(0) == 0.0

    def test_square_root_one(self):
        """Test square root of one."""
        assert square_root(1) == 1.0

    def test_square_root_two(self):
        """Test square root of two."""
        assert square_root(2) == pytest.approx(1.414, abs=1e-3)

    def test_square_root_float(self):
        """Test square root of float."""
        result = square_root(0.25)
        assert result == pytest.approx(0.5)

    def test_square_root_large_number(self):
        """Test square root of large number."""
        result = square_root(1e10)
        assert result == pytest.approx(1e5)

    def test_square_root_small_number(self):
        """Test square root of small number."""
        result = square_root(1e-10)
        assert result == pytest.approx(1e-5)

    def test_square_root_negative_raises_error(self):
        """Test that square root of negative raises ValueError."""
        with pytest.raises(ValueError, match="not defined for negative values"):
            square_root(-1)

    def test_square_root_very_negative_raises_error(self):
        """Test that square root of very negative number raises error."""
        with pytest.raises(ValueError):
            square_root(-100)

    def test_square_root_inverse_of_square(self):
        """Test that square root is inverse of square."""
        for value in [0, 1, 5, 10, 0.5, 100]:
            assert square_root(square(value)) == pytest.approx(value)

    def test_square_root_property(self):
        """Test square root property: sqrt(a*b) = sqrt(a) * sqrt(b)."""
        a = 4
        b = 9
        assert square_root(a * b) == pytest.approx(square_root(a) * square_root(b))


class TestCubeRootFunction:
    """Test the cube_root pure function."""

    def test_cube_root_perfect_cube(self):
        """Test cube root of perfect cube."""
        assert cube_root(8) == pytest.approx(2.0)

    def test_cube_root_zero(self):
        """Test cube root of zero."""
        assert cube_root(0) == 0.0

    def test_cube_root_one(self):
        """Test cube root of one."""
        assert cube_root(1) == pytest.approx(1.0)

    def test_cube_root_negative_one(self):
        """Test cube root of negative one."""
        assert cube_root(-1) == pytest.approx(-1.0)

    def test_cube_root_negative_eight(self):
        """Test cube root of negative eight."""
        assert cube_root(-8) == pytest.approx(-2.0)

    def test_cube_root_positive(self):
        """Test cube root of positive number."""
        result = cube_root(27)
        assert result == pytest.approx(3.0)

    def test_cube_root_negative(self):
        """Test cube root of negative number."""
        result = cube_root(-27)
        assert result == pytest.approx(-3.0)

    def test_cube_root_fractional_positive(self):
        """Test cube root of positive fraction."""
        result = cube_root(0.125)
        assert result == pytest.approx(0.5)

    def test_cube_root_fractional_negative(self):
        """Test cube root of negative fraction."""
        result = cube_root(-0.125)
        assert result == pytest.approx(-0.5)

    def test_cube_root_large_number(self):
        """Test cube root of large number."""
        result = cube_root(1e15)
        assert result == pytest.approx(1e5)

    def test_cube_root_small_number(self):
        """Test cube root of small number."""
        result = cube_root(1e-15)
        assert result == pytest.approx(1e-5)

    def test_cube_root_preserves_sign(self):
        """Test that cube root preserves sign of input."""
        assert cube_root(8) > 0
        assert cube_root(-8) < 0
        assert cube_root(0) == 0

    def test_cube_root_inverse_of_cube(self):
        """Test that cube root is inverse of cube."""
        for value in [-10, -1, 0, 1, 5, 10, 0.5, -0.5]:
            assert cube_root(cube(value)) == pytest.approx(value)

    def test_cube_root_property(self):
        """Test cube root property: cbrt(a*b) ≈ cbrt(a) * cbrt(b)."""
        a = 8
        b = 27
        assert cube_root(a * b) == pytest.approx(cube_root(a) * cube_root(b))

    def test_cube_root_two(self):
        """Test cube root of two."""
        result = cube_root(2)
        assert result == pytest.approx(1.26, abs=1e-2)


class TestRootsEdgeCases:
    """Test edge cases for root functions."""

    def test_square_then_square_root(self):
        """Test that sqrt(x^2) = |x|."""
        assert square_root(square(5)) == 5
        assert square_root(square(-5)) == 5

    def test_cube_then_cube_root(self):
        """Test that cbrt(x^3) = x."""
        for value in [-5, -1, 0, 1, 5]:
            assert cube_root(cube(value)) == pytest.approx(value)

    def test_large_factorial_computation(self):
        """Test factorial for reasonable large values."""
        assert factorial(15) == 1307674368000

    def test_square_root_of_very_large_number(self):
        """Test square root computation stability."""
        large_num = 1e300
        result = square_root(large_num)
        assert result == pytest.approx(1e150)

    def test_cube_root_of_very_large_number(self):
        """Test cube root computation stability."""
        large_num = 1e300
        result = cube_root(large_num)
        assert result == pytest.approx(1e100)

    def test_multiple_square_roots(self):
        """Test applying square root multiple times."""
        value = 256
        # sqrt(256) = 16
        result = square_root(value)
        assert result == pytest.approx(16.0)
        # sqrt(16) = 4
        result = square_root(result)
        assert result == pytest.approx(4.0)
        # sqrt(4) = 2
        result = square_root(result)
        assert result == pytest.approx(2.0)

    def test_multiple_cube_roots(self):
        """Test applying cube root multiple times."""
        value = 512  # 2^9
        # cbrt(512) = 8
        result = cube_root(value)
        assert result == pytest.approx(8.0)
        # cbrt(8) = 2
        result = cube_root(result)
        assert result == pytest.approx(2.0)
