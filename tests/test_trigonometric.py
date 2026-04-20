"""Comprehensive tests for trigonometric functions in Calculator.

Tests cover:
- sin(x) function with various inputs
- cos(x) function with various inputs
- tan(x) function with various inputs
- Trigonometric identities verification
- Edge cases (zero, multiples of pi, special angles)
- Negative angles
- Large values
- Chaining trigonometric results
"""

import pytest
import math
from src.calculator import Calculator


@pytest.fixture
def calc():
    """Provide a Calculator instance."""
    return Calculator()


class TestSineFunction:
    """Test suite for Calculator.sin() method."""

    def test_sin_zero(self, calc):
        """Verify that sin(0) equals 0."""
        result = calc.sin(0)
        assert abs(result) < 1e-10

    def test_sin_pi_half(self, calc):
        """Verify that sin(π/2) equals 1."""
        result = calc.sin(math.pi / 2)
        assert abs(result - 1.0) < 1e-10

    def test_sin_pi(self, calc):
        """Verify that sin(π) equals 0."""
        result = calc.sin(math.pi)
        assert abs(result) < 1e-10

    def test_sin_three_pi_half(self, calc):
        """Verify that sin(3π/2) equals -1."""
        result = calc.sin(3 * math.pi / 2)
        assert abs(result - (-1.0)) < 1e-10

    def test_sin_two_pi(self, calc):
        """Verify that sin(2π) equals 0."""
        result = calc.sin(2 * math.pi)
        assert abs(result) < 1e-10

    def test_sin_negative_angle(self, calc):
        """Verify that sin(-x) equals -sin(x)."""
        x = math.pi / 6
        sin_pos = calc.sin(x)
        sin_neg = calc.sin(-x)
        assert abs(sin_pos + sin_neg) < 1e-10

    def test_sin_quarter_pi(self, calc):
        """Verify that sin(π/4) equals √2/2."""
        result = calc.sin(math.pi / 4)
        expected = math.sqrt(2) / 2
        assert abs(result - expected) < 1e-10

    def test_sin_sixth_pi(self, calc):
        """Verify that sin(π/6) equals 0.5."""
        result = calc.sin(math.pi / 6)
        assert abs(result - 0.5) < 1e-10

    def test_sin_third_pi(self, calc):
        """Verify that sin(π/3) equals √3/2."""
        result = calc.sin(math.pi / 3)
        expected = math.sqrt(3) / 2
        assert abs(result - expected) < 1e-10

    def test_sin_negative_pi_half(self, calc):
        """Verify that sin(-π/2) equals -1."""
        result = calc.sin(-math.pi / 2)
        assert abs(result - (-1.0)) < 1e-10

    def test_sin_small_positive_float(self, calc):
        """Verify sin() with small positive float."""
        result = calc.sin(0.1)
        expected = math.sin(0.1)
        assert abs(result - expected) < 1e-10

    def test_sin_small_negative_float(self, calc):
        """Verify sin() with small negative float."""
        result = calc.sin(-0.1)
        expected = math.sin(-0.1)
        assert abs(result - expected) < 1e-10

    def test_sin_large_angle(self, calc):
        """Verify sin() with large angle (periodicity)."""
        # sin(x) = sin(x + 2π)
        x = 5.5
        result1 = calc.sin(x)
        result2 = calc.sin(x + 2 * math.pi)
        assert abs(result1 - result2) < 1e-10

    def test_sin_returns_float(self, calc):
        """Verify that sin() returns a float."""
        result = calc.sin(1.0)
        assert isinstance(result, float)

    def test_sin_range_is_minus_one_to_one(self, calc):
        """Verify that sin() result is always in [-1, 1]."""
        test_angles = [0, 0.5, 1.0, math.pi, 2 * math.pi, -math.pi]
        for angle in test_angles:
            result = calc.sin(angle)
            assert -1.0 <= result <= 1.0


class TestCosineFunction:
    """Test suite for Calculator.cos() method."""

    def test_cos_zero(self, calc):
        """Verify that cos(0) equals 1."""
        result = calc.cos(0)
        assert abs(result - 1.0) < 1e-10

    def test_cos_pi_half(self, calc):
        """Verify that cos(π/2) equals 0."""
        result = calc.cos(math.pi / 2)
        assert abs(result) < 1e-10

    def test_cos_pi(self, calc):
        """Verify that cos(π) equals -1."""
        result = calc.cos(math.pi)
        assert abs(result - (-1.0)) < 1e-10

    def test_cos_three_pi_half(self, calc):
        """Verify that cos(3π/2) equals 0."""
        result = calc.cos(3 * math.pi / 2)
        assert abs(result) < 1e-10

    def test_cos_two_pi(self, calc):
        """Verify that cos(2π) equals 1."""
        result = calc.cos(2 * math.pi)
        assert abs(result - 1.0) < 1e-10

    def test_cos_even_function(self, calc):
        """Verify that cos(-x) equals cos(x) (even function)."""
        x = math.pi / 6
        cos_pos = calc.cos(x)
        cos_neg = calc.cos(-x)
        assert abs(cos_pos - cos_neg) < 1e-10

    def test_cos_quarter_pi(self, calc):
        """Verify that cos(π/4) equals √2/2."""
        result = calc.cos(math.pi / 4)
        expected = math.sqrt(2) / 2
        assert abs(result - expected) < 1e-10

    def test_cos_sixth_pi(self, calc):
        """Verify that cos(π/6) equals √3/2."""
        result = calc.cos(math.pi / 6)
        expected = math.sqrt(3) / 2
        assert abs(result - expected) < 1e-10

    def test_cos_third_pi(self, calc):
        """Verify that cos(π/3) equals 0.5."""
        result = calc.cos(math.pi / 3)
        assert abs(result - 0.5) < 1e-10

    def test_cos_negative_pi(self, calc):
        """Verify that cos(-π) equals -1."""
        result = calc.cos(-math.pi)
        assert abs(result - (-1.0)) < 1e-10

    def test_cos_small_positive_float(self, calc):
        """Verify cos() with small positive float."""
        result = calc.cos(0.1)
        expected = math.cos(0.1)
        assert abs(result - expected) < 1e-10

    def test_cos_small_negative_float(self, calc):
        """Verify cos() with small negative float."""
        result = calc.cos(-0.1)
        expected = math.cos(-0.1)
        assert abs(result - expected) < 1e-10

    def test_cos_large_angle(self, calc):
        """Verify cos() with large angle (periodicity)."""
        # cos(x) = cos(x + 2π)
        x = 5.5
        result1 = calc.cos(x)
        result2 = calc.cos(x + 2 * math.pi)
        assert abs(result1 - result2) < 1e-10

    def test_cos_returns_float(self, calc):
        """Verify that cos() returns a float."""
        result = calc.cos(1.0)
        assert isinstance(result, float)

    def test_cos_range_is_minus_one_to_one(self, calc):
        """Verify that cos() result is always in [-1, 1]."""
        test_angles = [0, 0.5, 1.0, math.pi, 2 * math.pi, -math.pi]
        for angle in test_angles:
            result = calc.cos(angle)
            assert -1.0 <= result <= 1.0


class TestTangentFunction:
    """Test suite for Calculator.tan() method."""

    def test_tan_zero(self, calc):
        """Verify that tan(0) equals 0."""
        result = calc.tan(0)
        assert abs(result) < 1e-10

    def test_tan_pi_quarter(self, calc):
        """Verify that tan(π/4) equals 1."""
        result = calc.tan(math.pi / 4)
        assert abs(result - 1.0) < 1e-10

    def test_tan_pi(self, calc):
        """Verify that tan(π) equals 0."""
        result = calc.tan(math.pi)
        assert abs(result) < 1e-10

    def test_tan_negative_angle(self, calc):
        """Verify that tan(-x) equals -tan(x)."""
        x = math.pi / 6
        tan_pos = calc.tan(x)
        tan_neg = calc.tan(-x)
        assert abs(tan_pos + tan_neg) < 1e-10

    def test_tan_sixth_pi(self, calc):
        """Verify that tan(π/6) equals 1/√3."""
        result = calc.tan(math.pi / 6)
        expected = 1.0 / math.sqrt(3)
        assert abs(result - expected) < 1e-10

    def test_tan_third_pi(self, calc):
        """Verify that tan(π/3) equals √3."""
        result = calc.tan(math.pi / 3)
        expected = math.sqrt(3)
        assert abs(result - expected) < 1e-10

    def test_tan_negative_quarter_pi(self, calc):
        """Verify that tan(-π/4) equals -1."""
        result = calc.tan(-math.pi / 4)
        assert abs(result - (-1.0)) < 1e-10

    def test_tan_small_positive_float(self, calc):
        """Verify tan() with small positive float."""
        result = calc.tan(0.1)
        expected = math.tan(0.1)
        assert abs(result - expected) < 1e-10

    def test_tan_small_negative_float(self, calc):
        """Verify tan() with small negative float."""
        result = calc.tan(-0.1)
        expected = math.tan(-0.1)
        assert abs(result - expected) < 1e-10

    def test_tan_periodicity(self, calc):
        """Verify tan() periodicity: tan(x) = tan(x + π)."""
        x = 0.5
        result1 = calc.tan(x)
        result2 = calc.tan(x + math.pi)
        assert abs(result1 - result2) < 1e-10

    def test_tan_returns_float(self, calc):
        """Verify that tan() returns a float."""
        result = calc.tan(1.0)
        assert isinstance(result, float)

    def test_tan_near_pi_half(self, calc):
        """Verify tan() near π/2 (where it approaches infinity)."""
        # tan(π/2 - epsilon) is very large
        x = math.pi / 2 - 0.01
        result = calc.tan(x)
        assert result > 50  # Should be very large


class TestTrigonometricIdentities:
    """Test trigonometric identities to verify correctness."""

    def test_pythagorean_identity(self, calc):
        """Verify sin²(x) + cos²(x) = 1."""
        test_angles = [0, 0.5, 1.0, math.pi / 4, math.pi / 6, math.pi / 3, math.pi / 2]
        for angle in test_angles:
            sin_val = calc.sin(angle)
            cos_val = calc.cos(angle)
            result = sin_val ** 2 + cos_val ** 2
            assert abs(result - 1.0) < 1e-10

    def test_tan_as_sin_over_cos(self, calc):
        """Verify tan(x) = sin(x) / cos(x) for various angles."""
        test_angles = [0.1, 0.5, 1.0, math.pi / 4, math.pi / 6, math.pi / 3]
        for angle in test_angles:
            tan_val = calc.tan(angle)
            sin_val = calc.sin(angle)
            cos_val = calc.cos(angle)
            expected = sin_val / cos_val
            assert abs(tan_val - expected) < 1e-10

    def test_sin_plus_cos_identity(self, calc):
        """Verify sin²(x/2) = (1 - cos(x)) / 2 (half-angle variant)."""
        x = 1.0
        sin_half = calc.sin(x / 2)
        cos_x = calc.cos(x)
        expected = sin_half ** 2
        computed = (1 - cos_x) / 2
        assert abs(expected - computed) < 1e-10


class TestTrigonometricChaining:
    """Test that trigonometric results can be chained."""

    def test_sin_result_chains_to_cos(self, calc):
        """Verify sin() result can be input to cos()."""
        result_sin = calc.sin(math.pi / 4)
        result_cos = calc.cos(result_sin)
        assert isinstance(result_cos, float)

    def test_cos_result_chains_to_sin(self, calc):
        """Verify cos() result can be input to sin()."""
        result_cos = calc.cos(math.pi / 4)
        result_sin = calc.sin(result_cos)
        assert isinstance(result_sin, float)

    def test_tan_result_chains_to_sin(self, calc):
        """Verify tan() result can be input to sin()."""
        result_tan = calc.tan(math.pi / 4)
        result_sin = calc.sin(result_tan)
        assert isinstance(result_sin, float)

    def test_multiple_trig_chaining(self, calc):
        """Verify chaining multiple trigonometric operations."""
        x = 0.5
        result = calc.sin(x)
        result = calc.cos(result)
        result = calc.tan(result)
        assert isinstance(result, float)

    def test_trig_with_arithmetic_operations(self, calc):
        """Verify trigonometric results work with arithmetic operations."""
        sin_result = calc.sin(math.pi / 4)
        cos_result = calc.cos(math.pi / 4)
        # Both should be √2/2
        sum_result = calc.add(sin_result, cos_result)
        expected = math.sqrt(2)
        assert abs(sum_result - expected) < 1e-10


class TestTrigonometricEdgeCases:
    """Test edge cases for trigonometric functions."""

    def test_sin_very_large_angle(self, calc):
        """Verify sin() with very large angle."""
        x = 1000.0
        result = calc.sin(x)
        assert -1.0 <= result <= 1.0

    def test_cos_very_large_angle(self, calc):
        """Verify cos() with very large angle."""
        x = 1000.0
        result = calc.cos(x)
        assert -1.0 <= result <= 1.0

    def test_tan_very_large_angle(self, calc):
        """Verify tan() with very large angle."""
        x = 1000.0
        result = calc.tan(x)
        assert isinstance(result, float)

    def test_sin_very_small_angle(self, calc):
        """Verify sin(x) ≈ x for very small x."""
        x = 0.00001
        result = calc.sin(x)
        assert abs(result - x) < 1e-9

    def test_cos_very_small_angle(self, calc):
        """Verify cos(x) ≈ 1 for very small x."""
        x = 0.00001
        result = calc.cos(x)
        assert abs(result - 1.0) < 1e-8

    def test_sin_negative_large_angle(self, calc):
        """Verify sin() with negative large angle."""
        x = -1000.0
        result = calc.sin(x)
        assert -1.0 <= result <= 1.0

    def test_cos_negative_large_angle(self, calc):
        """Verify cos() with negative large angle."""
        x = -1000.0
        result = calc.cos(x)
        assert -1.0 <= result <= 1.0
