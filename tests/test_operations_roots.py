"""Comprehensive tests for root extraction operations module.

Tests cover square root and cube root with normal cases, edge cases,
and error conditions.
"""

import pytest
import math
from src.operations import roots


class TestSquareRoot:
    """Test suite for roots.square_root()"""

    def test_square_root_perfect_square(self):
        """Happy path: square root of perfect squares."""
        assert roots.square_root(4) == 2.0
        assert roots.square_root(9) == 3.0
        assert roots.square_root(16) == 4.0
        assert roots.square_root(100) == 10.0

    def test_square_root_zero(self):
        """Square root of zero is zero."""
        assert roots.square_root(0) == 0.0

    def test_square_root_one(self):
        """Square root of one is one."""
        assert roots.square_root(1) == 1.0

    def test_square_root_non_perfect_square(self):
        """Square root of non-perfect squares."""
        result = roots.square_root(2)
        assert abs(result - math.sqrt(2)) < 1e-10

    def test_square_root_positive_float(self):
        """Square root of positive float."""
        result = roots.square_root(2.25)
        assert abs(result - 1.5) < 1e-10

    def test_square_root_small_positive(self):
        """Square root of small positive number."""
        result = roots.square_root(0.01)
        assert abs(result - 0.1) < 1e-10

    def test_square_root_large_number(self):
        """Square root of large number."""
        result = roots.square_root(10**10)
        assert abs(result - 10**5) < 1e-5

    def test_square_root_very_small_positive(self):
        """Square root of very small positive number."""
        small = 1e-20
        result = roots.square_root(small)
        assert abs(result - math.sqrt(small)) < 1e-30

    def test_square_root_negative_raises_error(self):
        """Square root of negative number raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            roots.square_root(-1)
        assert "square_root requires a non-negative number" in str(exc_info.value)
        assert "-1" in str(exc_info.value)

    def test_square_root_large_negative_raises_error(self):
        """Square root of large negative number raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            roots.square_root(-100)
        assert "square_root requires a non-negative number" in str(exc_info.value)

    def test_square_root_small_negative_raises_error(self):
        """Square root of small negative number raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            roots.square_root(-0.001)
        assert "square_root requires a non-negative number" in str(exc_info.value)

    def test_square_root_negative_zero(self):
        """Square root of negative zero (mathematically same as zero)."""
        # In Python, -0.0 == 0.0 in comparison, but let's test it
        result = roots.square_root(-0.0)
        assert result == 0.0

    def test_square_root_infinity(self):
        """Square root of positive infinity."""
        result = roots.square_root(float('inf'))
        assert result == float('inf')

    def test_square_root_negative_infinity_raises_error(self):
        """Square root of negative infinity raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            roots.square_root(float('-inf'))
        assert "square_root requires a non-negative number" in str(exc_info.value)

    def test_square_root_nan_propagates(self):
        """Square root of NaN propagates NaN."""
        # NaN is not < 0, so it won't raise ValueError
        result = roots.square_root(float('nan'))
        assert math.isnan(result)

    def test_square_root_string_raises_error(self):
        """String input should raise TypeError."""
        with pytest.raises(TypeError):
            roots.square_root("4")

    def test_square_root_none_raises_error(self):
        """None input should raise TypeError."""
        with pytest.raises(TypeError):
            roots.square_root(None)

    def test_square_root_list_raises_error(self):
        """List input should raise TypeError."""
        with pytest.raises(TypeError):
            roots.square_root([4])

    def test_square_root_inverse_of_square(self):
        """sqrt(x^2) = |x|."""
        x = 7
        result = roots.square_root(x ** 2)
        assert abs(result - x) < 1e-10

    def test_square_root_inverse_of_square_negative(self):
        """sqrt((-x)^2) = |(-x)| = x."""
        x = -7
        result = roots.square_root(x ** 2)
        assert abs(result - abs(x)) < 1e-10

    def test_square_root_result_always_non_negative(self):
        """Result of square root is always non-negative (or NaN/inf)."""
        assert roots.square_root(25) >= 0
        assert roots.square_root(0.0001) >= 0

    def test_square_root_very_large_perfect_square(self):
        """Square root of very large perfect square."""
        large = 10**100
        result = roots.square_root(large)
        assert abs(result - 10**50) < 1e-40


class TestCubeRoot:
    """Test suite for roots.cube_root()"""

    def test_cube_root_perfect_cube(self):
        """Happy path: cube root of perfect cubes."""
        # Using approximate comparison due to floating point precision
        assert abs(roots.cube_root(8) - 2.0) < 1e-10
        assert abs(roots.cube_root(27) - 3.0) < 1e-10
        assert abs(roots.cube_root(64) - 4.0) < 1e-10

    def test_cube_root_zero(self):
        """Cube root of zero is zero."""
        assert roots.cube_root(0) == 0.0

    def test_cube_root_one(self):
        """Cube root of one is one."""
        assert roots.cube_root(1) == 1.0

    def test_cube_root_negative_one(self):
        """Cube root of negative one is negative one."""
        result = roots.cube_root(-1)
        assert abs(result - (-1.0)) < 1e-10

    def test_cube_root_negative_perfect_cube(self):
        """Cube root of negative perfect cube (Python 3.12 cbrt supports negative)."""
        result = roots.cube_root(-8)
        assert abs(result - (-2.0)) < 1e-10

    def test_cube_root_negative_27(self):
        """Cube root of -27."""
        result = roots.cube_root(-27)
        assert abs(result - (-3.0)) < 1e-10

    def test_cube_root_positive_float(self):
        """Cube root of positive float."""
        result = roots.cube_root(8.0)
        assert abs(result - 2.0) < 1e-10

    def test_cube_root_non_perfect_cube(self):
        """Cube root of non-perfect cube."""
        result = roots.cube_root(10)
        expected = 10 ** (1/3)
        assert abs(result - expected) < 1e-10

    def test_cube_root_small_positive(self):
        """Cube root of small positive number."""
        result = roots.cube_root(0.001)
        assert abs(result - 0.1) < 1e-10

    def test_cube_root_large_positive(self):
        """Cube root of large positive number."""
        result = roots.cube_root(10**12)
        assert abs(result - 10**4) < 1e-5

    def test_cube_root_very_small_positive(self):
        """Cube root of very small positive number."""
        small = 1e-30
        result = roots.cube_root(small)
        assert abs(result - 1e-10) < 1e-20

    def test_cube_root_small_negative(self):
        """Cube root of small negative number."""
        result = roots.cube_root(-0.001)
        assert abs(result - (-0.1)) < 1e-10

    def test_cube_root_very_small_negative(self):
        """Cube root of very small negative number."""
        small = -1e-30
        result = roots.cube_root(small)
        assert abs(result - (-1e-10)) < 1e-20

    def test_cube_root_large_negative(self):
        """Cube root of large negative number."""
        result = roots.cube_root(-10**12)
        assert abs(result - (-10**4)) < 1e-5

    def test_cube_root_infinity(self):
        """Cube root of positive infinity."""
        result = roots.cube_root(float('inf'))
        assert result == float('inf')

    def test_cube_root_negative_infinity(self):
        """Cube root of negative infinity."""
        result = roots.cube_root(float('-inf'))
        assert result == float('-inf')

    def test_cube_root_nan_propagates(self):
        """Cube root of NaN."""
        result = roots.cube_root(float('nan'))
        assert math.isnan(result)

    def test_cube_root_string_raises_error(self):
        """String input should raise TypeError."""
        with pytest.raises(TypeError):
            roots.cube_root("8")

    def test_cube_root_none_raises_error(self):
        """None input should raise TypeError."""
        with pytest.raises(TypeError):
            roots.cube_root(None)

    def test_cube_root_list_raises_error(self):
        """List input should raise TypeError."""
        with pytest.raises(TypeError):
            roots.cube_root([8])

    def test_cube_root_inverse_of_cube(self):
        """cbrt(x^3) = x."""
        x = 5
        result = roots.cube_root(x ** 3)
        assert abs(result - x) < 1e-10

    def test_cube_root_inverse_of_cube_negative(self):
        """cbrt((-x)^3) = -x."""
        x = 5
        result = roots.cube_root((-x) ** 3)
        assert abs(result - (-x)) < 1e-10

    def test_cube_root_preserves_sign(self):
        """Cube root preserves sign of input."""
        positive_result = roots.cube_root(8)
        negative_result = roots.cube_root(-8)
        assert positive_result > 0
        assert negative_result < 0

    def test_cube_root_very_large_perfect_cube(self):
        """Cube root of very large perfect cube."""
        large = 10**100
        result = roots.cube_root(large)
        # cbrt(10^100) should be approximately 10^(100/3)
        expected = large ** (1/3)
        # Use looser tolerance for very large numbers (floating point limits)
        assert abs(result - expected) < 1e-10 * abs(expected)

    def test_cube_root_monotonic_increasing(self):
        """Cube root is monotonically increasing."""
        assert roots.cube_root(-8) < roots.cube_root(0)
        assert roots.cube_root(0) < roots.cube_root(8)


class TestRootsIntegration:
    """Integration tests combining root operations."""

    def test_square_root_inverse_of_square(self):
        """sqrt(x**2) = |x|."""
        from src.operations import exponents
        x = 9
        squared = exponents.square(x)
        result = roots.square_root(squared)
        assert abs(result - x) < 1e-10

    def test_cube_root_inverse_of_cube(self):
        """cbrt(x**3) = x."""
        from src.operations import exponents
        x = 7
        cubed = exponents.cube(x)
        result = roots.cube_root(cubed)
        assert abs(result - x) < 1e-10

    def test_cube_root_inverse_of_cube_negative(self):
        """cbrt((-x)**3) = -x."""
        from src.operations import exponents
        x = 7
        neg_cubed = exponents.cube(-x)
        result = roots.cube_root(neg_cubed)
        assert abs(result - (-x)) < 1e-10

    def test_nested_roots(self):
        """Nested roots: cbrt(sqrt(x^6)) = x."""
        from src.operations import exponents
        x = 4
        x_6 = exponents.power(x, 6)
        sqrt_x_6 = roots.square_root(x_6)
        result = roots.cube_root(sqrt_x_6)
        assert abs(result - x) < 1e-10

    def test_square_root_and_square_composition(self):
        """Composing square root and square."""
        from src.operations import exponents
        x = 16
        # sqrt(x) then square it
        sqrt_x = roots.square_root(x)
        squared = exponents.square(sqrt_x)
        assert abs(squared - x) < 1e-10

    def test_cube_root_monotonicity_with_operations(self):
        """Cube root maintains order of inputs."""
        from src.operations import exponents
        a, b = 2, 3
        a_cubed = exponents.cube(a)
        b_cubed = exponents.cube(b)
        assert roots.cube_root(a_cubed) < roots.cube_root(b_cubed)

    def test_square_root_no_domain_for_negatives(self):
        """Square root has strict domain restriction."""
        from src.operations import exponents
        # Negative inputs to square_root raise ValueError
        x = -5
        with pytest.raises(ValueError):
            roots.square_root(x)

    def test_cube_root_all_reals(self):
        """Cube root works on all real numbers."""
        from src.operations import exponents
        # Both positive and negative work fine
        assert roots.cube_root(8) > 0
        assert roots.cube_root(-8) < 0
        assert roots.cube_root(0) == 0
