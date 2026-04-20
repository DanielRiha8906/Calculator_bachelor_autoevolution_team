"""Comprehensive tests for scientific methods in ArithmeticEngine.

Tests cover:
- sin, cos, tan, exp, log, sqrt methods
- Type checking (bool/non-numeric inputs raise TypeError)
- Domain violations (negative log/sqrt, tan at odd multiples of pi/2 raise ValueError)
- Accuracy of trigonometric and transcendental functions
"""

import pytest
import math
from src.logic.core import ArithmeticEngine


@pytest.fixture
def engine():
    """Provides a fresh ArithmeticEngine instance for each test."""
    return ArithmeticEngine()


# ============================================================================
# SINE OPERATION TESTS
# ============================================================================

class TestSin:
    """Test suite for the sine operation."""

    def test_sin_zero(self, engine):
        """Test sin(0) == 0."""
        assert engine.sin(0) == pytest.approx(0.0)

    def test_sin_pi_over_2(self, engine):
        """Test sin(pi/2) == 1."""
        assert engine.sin(math.pi / 2) == pytest.approx(1.0)

    def test_sin_pi(self, engine):
        """Test sin(pi) == 0."""
        assert engine.sin(math.pi) == pytest.approx(0.0, abs=1e-9)

    def test_sin_3pi_over_2(self, engine):
        """Test sin(3*pi/2) == -1."""
        assert engine.sin(3 * math.pi / 2) == pytest.approx(-1.0)

    def test_sin_pi_over_6(self, engine):
        """Test sin(pi/6) == 0.5."""
        assert engine.sin(math.pi / 6) == pytest.approx(0.5)

    def test_sin_pi_over_4(self, engine):
        """Test sin(pi/4) == sqrt(2)/2."""
        assert engine.sin(math.pi / 4) == pytest.approx(math.sqrt(2) / 2)

    def test_sin_negative_angle(self, engine):
        """Test sin(-pi/2) == -1."""
        assert engine.sin(-math.pi / 2) == pytest.approx(-1.0)

    def test_sin_large_angle(self, engine):
        """Test sin with large angle."""
        assert engine.sin(10 * math.pi) == pytest.approx(0.0, abs=1e-9)

    def test_sin_float_input(self, engine):
        """Test sin with float input."""
        assert engine.sin(1.5) == pytest.approx(math.sin(1.5))

    def test_sin_returns_float(self, engine):
        """Test that sin always returns float."""
        result = engine.sin(0)
        assert isinstance(result, float)

    def test_sin_bool_raises_typeerror(self, engine):
        """Test that bool input raises TypeError."""
        with pytest.raises(TypeError):
            engine.sin(True)
        with pytest.raises(TypeError):
            engine.sin(False)

    def test_sin_none_raises_typeerror(self, engine):
        """Test that None input raises TypeError."""
        with pytest.raises(TypeError):
            engine.sin(None)

    def test_sin_string_raises_typeerror(self, engine):
        """Test that string input raises TypeError."""
        with pytest.raises(TypeError):
            engine.sin("0")
        with pytest.raises(TypeError):
            engine.sin("")

    def test_sin_list_raises_typeerror(self, engine):
        """Test that list input raises TypeError."""
        with pytest.raises(TypeError):
            engine.sin([0])


# ============================================================================
# COSINE OPERATION TESTS
# ============================================================================

class TestCos:
    """Test suite for the cosine operation."""

    def test_cos_zero(self, engine):
        """Test cos(0) == 1."""
        assert engine.cos(0) == pytest.approx(1.0)

    def test_cos_pi_over_2(self, engine):
        """Test cos(pi/2) == 0."""
        assert engine.cos(math.pi / 2) == pytest.approx(0.0, abs=1e-9)

    def test_cos_pi(self, engine):
        """Test cos(pi) == -1."""
        assert engine.cos(math.pi) == pytest.approx(-1.0)

    def test_cos_3pi_over_2(self, engine):
        """Test cos(3*pi/2) == 0."""
        assert engine.cos(3 * math.pi / 2) == pytest.approx(0.0, abs=1e-9)

    def test_cos_pi_over_3(self, engine):
        """Test cos(pi/3) == 0.5."""
        assert engine.cos(math.pi / 3) == pytest.approx(0.5)

    def test_cos_pi_over_4(self, engine):
        """Test cos(pi/4) == sqrt(2)/2."""
        assert engine.cos(math.pi / 4) == pytest.approx(math.sqrt(2) / 2)

    def test_cos_negative_angle(self, engine):
        """Test cos(-pi) == -1."""
        assert engine.cos(-math.pi) == pytest.approx(-1.0)

    def test_cos_large_angle(self, engine):
        """Test cos with large angle."""
        assert engine.cos(10 * math.pi) == pytest.approx(1.0)

    def test_cos_float_input(self, engine):
        """Test cos with float input."""
        assert engine.cos(1.5) == pytest.approx(math.cos(1.5))

    def test_cos_returns_float(self, engine):
        """Test that cos always returns float."""
        result = engine.cos(0)
        assert isinstance(result, float)

    def test_cos_bool_raises_typeerror(self, engine):
        """Test that bool input raises TypeError."""
        with pytest.raises(TypeError):
            engine.cos(True)
        with pytest.raises(TypeError):
            engine.cos(False)

    def test_cos_none_raises_typeerror(self, engine):
        """Test that None input raises TypeError."""
        with pytest.raises(TypeError):
            engine.cos(None)

    def test_cos_string_raises_typeerror(self, engine):
        """Test that string input raises TypeError."""
        with pytest.raises(TypeError):
            engine.cos("0")

    def test_cos_list_raises_typeerror(self, engine):
        """Test that list input raises TypeError."""
        with pytest.raises(TypeError):
            engine.cos([0])


# ============================================================================
# TANGENT OPERATION TESTS
# ============================================================================

class TestTan:
    """Test suite for the tangent operation."""

    def test_tan_zero(self, engine):
        """Test tan(0) == 0."""
        assert engine.tan(0) == pytest.approx(0.0)

    def test_tan_pi_over_4(self, engine):
        """Test tan(pi/4) == 1."""
        assert engine.tan(math.pi / 4) == pytest.approx(1.0)

    def test_tan_pi(self, engine):
        """Test tan(pi) == 0."""
        assert engine.tan(math.pi) == pytest.approx(0.0, abs=1e-9)

    def test_tan_pi_over_6(self, engine):
        """Test tan(pi/6) == 1/sqrt(3)."""
        assert engine.tan(math.pi / 6) == pytest.approx(1 / math.sqrt(3))

    def test_tan_negative_angle(self, engine):
        """Test tan(-pi/4) == -1."""
        assert engine.tan(-math.pi / 4) == pytest.approx(-1.0)

    def test_tan_float_input(self, engine):
        """Test tan with float input."""
        assert engine.tan(0.5) == pytest.approx(math.tan(0.5))

    def test_tan_returns_float(self, engine):
        """Test that tan always returns float."""
        result = engine.tan(0)
        assert isinstance(result, float)

    def test_tan_pi_over_2_raises_valueerror(self, engine):
        """Test that tan(pi/2) raises ValueError."""
        with pytest.raises(ValueError):
            engine.tan(math.pi / 2)

    def test_tan_3pi_over_2_raises_valueerror(self, engine):
        """Test that tan(3*pi/2) raises ValueError."""
        with pytest.raises(ValueError):
            engine.tan(3 * math.pi / 2)

    def test_tan_negative_pi_over_2_raises_valueerror(self, engine):
        """Test that tan(-pi/2) raises ValueError."""
        with pytest.raises(ValueError):
            engine.tan(-math.pi / 2)

    def test_tan_bool_raises_typeerror(self, engine):
        """Test that bool input raises TypeError."""
        with pytest.raises(TypeError):
            engine.tan(True)
        with pytest.raises(TypeError):
            engine.tan(False)

    def test_tan_none_raises_typeerror(self, engine):
        """Test that None input raises TypeError."""
        with pytest.raises(TypeError):
            engine.tan(None)

    def test_tan_string_raises_typeerror(self, engine):
        """Test that string input raises TypeError."""
        with pytest.raises(TypeError):
            engine.tan("0")

    def test_tan_list_raises_typeerror(self, engine):
        """Test that list input raises TypeError."""
        with pytest.raises(TypeError):
            engine.tan([0])


# ============================================================================
# EXPONENTIAL OPERATION TESTS
# ============================================================================

class TestExp:
    """Test suite for the exponential operation."""

    def test_exp_zero(self, engine):
        """Test exp(0) == 1."""
        assert engine.exp(0) == pytest.approx(1.0)

    def test_exp_one(self, engine):
        """Test exp(1) == e."""
        assert engine.exp(1) == pytest.approx(math.e)

    def test_exp_negative_one(self, engine):
        """Test exp(-1) == 1/e."""
        assert engine.exp(-1) == pytest.approx(1 / math.e)

    def test_exp_two(self, engine):
        """Test exp(2) == e^2."""
        assert engine.exp(2) == pytest.approx(math.e ** 2)

    def test_exp_half(self, engine):
        """Test exp(0.5) == sqrt(e)."""
        assert engine.exp(0.5) == pytest.approx(math.sqrt(math.e))

    def test_exp_negative_number(self, engine):
        """Test exp with negative number approaches zero."""
        assert engine.exp(-10) == pytest.approx(math.exp(-10))

    def test_exp_large_number(self, engine):
        """Test exp with large number."""
        assert engine.exp(10) == pytest.approx(math.exp(10))

    def test_exp_float_input(self, engine):
        """Test exp with float input."""
        assert engine.exp(1.5) == pytest.approx(math.exp(1.5))

    def test_exp_returns_float(self, engine):
        """Test that exp always returns float."""
        result = engine.exp(0)
        assert isinstance(result, float)

    def test_exp_bool_raises_typeerror(self, engine):
        """Test that bool input raises TypeError."""
        with pytest.raises(TypeError):
            engine.exp(True)
        with pytest.raises(TypeError):
            engine.exp(False)

    def test_exp_none_raises_typeerror(self, engine):
        """Test that None input raises TypeError."""
        with pytest.raises(TypeError):
            engine.exp(None)

    def test_exp_string_raises_typeerror(self, engine):
        """Test that string input raises TypeError."""
        with pytest.raises(TypeError):
            engine.exp("0")

    def test_exp_list_raises_typeerror(self, engine):
        """Test that list input raises TypeError."""
        with pytest.raises(TypeError):
            engine.exp([0])


# ============================================================================
# NATURAL LOGARITHM OPERATION TESTS
# ============================================================================

class TestLog:
    """Test suite for the natural logarithm (base e) operation."""

    def test_log_one(self, engine):
        """Test log(1) == 0."""
        assert engine.log(1) == pytest.approx(0.0)

    def test_log_e(self, engine):
        """Test log(e) == 1."""
        assert engine.log(math.e) == pytest.approx(1.0)

    def test_log_e_squared(self, engine):
        """Test log(e^2) == 2."""
        assert engine.log(math.e ** 2) == pytest.approx(2.0)

    def test_log_sqrt_e(self, engine):
        """Test log(sqrt(e)) == 0.5."""
        assert engine.log(math.sqrt(math.e)) == pytest.approx(0.5, rel=1e-7)

    def test_log_one_over_e(self, engine):
        """Test log(1/e) == -1."""
        assert engine.log(1.0 / math.e) == pytest.approx(-1.0, rel=1e-7)

    def test_log_two(self, engine):
        """Test log(2) == ln(2)."""
        assert engine.log(2) == pytest.approx(math.log(2))

    def test_log_ten(self, engine):
        """Test log(10) == ln(10)."""
        assert engine.log(10) == pytest.approx(math.log(10))

    def test_log_very_small_positive(self, engine):
        """Test log of very small positive number."""
        assert engine.log(1e-5) == pytest.approx(math.log(1e-5))

    def test_log_large_positive(self, engine):
        """Test log of large positive number."""
        assert engine.log(1e5) == pytest.approx(math.log(1e5))

    def test_log_returns_float(self, engine):
        """Test that log always returns float."""
        result = engine.log(1)
        assert isinstance(result, float)

    def test_log_zero_raises_valueerror(self, engine):
        """Test that log(0) raises ValueError."""
        with pytest.raises(ValueError):
            engine.log(0)
        with pytest.raises(ValueError):
            engine.log(0.0)

    def test_log_negative_raises_valueerror(self, engine):
        """Test that log of negative raises ValueError."""
        with pytest.raises(ValueError):
            engine.log(-1)
        with pytest.raises(ValueError):
            engine.log(-10)
        with pytest.raises(ValueError):
            engine.log(-0.5)

    def test_log_bool_raises_typeerror(self, engine):
        """Test that bool input raises TypeError."""
        with pytest.raises(TypeError):
            engine.log(True)
        with pytest.raises(TypeError):
            engine.log(False)

    def test_log_none_raises_typeerror(self, engine):
        """Test that None input raises TypeError."""
        with pytest.raises(TypeError):
            engine.log(None)

    def test_log_string_raises_typeerror(self, engine):
        """Test that string input raises TypeError."""
        with pytest.raises(TypeError):
            engine.log("1")

    def test_log_list_raises_typeerror(self, engine):
        """Test that list input raises TypeError."""
        with pytest.raises(TypeError):
            engine.log([1])


# ============================================================================
# SQUARE ROOT OPERATION TESTS
# ============================================================================

class TestSqrt:
    """Test suite for the square root operation (scientific variant)."""

    def test_sqrt_zero(self, engine):
        """Test sqrt(0) == 0."""
        assert engine.sqrt(0) == pytest.approx(0.0)

    def test_sqrt_one(self, engine):
        """Test sqrt(1) == 1."""
        assert engine.sqrt(1) == pytest.approx(1.0)

    def test_sqrt_four(self, engine):
        """Test sqrt(4) == 2."""
        assert engine.sqrt(4) == pytest.approx(2.0)

    def test_sqrt_nine(self, engine):
        """Test sqrt(9) == 3."""
        assert engine.sqrt(9) == pytest.approx(3.0)

    def test_sqrt_two(self, engine):
        """Test sqrt(2) == sqrt(2)."""
        assert engine.sqrt(2) == pytest.approx(math.sqrt(2))

    def test_sqrt_quarter(self, engine):
        """Test sqrt(0.25) == 0.5."""
        assert engine.sqrt(0.25) == pytest.approx(0.5)

    def test_sqrt_hundred(self, engine):
        """Test sqrt(100) == 10."""
        assert engine.sqrt(100) == pytest.approx(10.0)

    def test_sqrt_large_number(self, engine):
        """Test sqrt of large number."""
        assert engine.sqrt(1e6) == pytest.approx(1e3)

    def test_sqrt_very_small_number(self, engine):
        """Test sqrt of very small positive number."""
        assert engine.sqrt(1e-4) == pytest.approx(1e-2)

    def test_sqrt_returns_float(self, engine):
        """Test that sqrt always returns float."""
        result = engine.sqrt(4)
        assert isinstance(result, float)

    def test_sqrt_negative_raises_valueerror(self, engine):
        """Test that sqrt of negative raises ValueError."""
        with pytest.raises(ValueError):
            engine.sqrt(-1)
        with pytest.raises(ValueError):
            engine.sqrt(-5)
        with pytest.raises(ValueError):
            engine.sqrt(-0.5)

    def test_sqrt_bool_raises_typeerror(self, engine):
        """Test that bool input raises TypeError."""
        with pytest.raises(TypeError):
            engine.sqrt(True)
        with pytest.raises(TypeError):
            engine.sqrt(False)

    def test_sqrt_none_raises_typeerror(self, engine):
        """Test that None input raises TypeError."""
        with pytest.raises(TypeError):
            engine.sqrt(None)

    def test_sqrt_string_raises_typeerror(self, engine):
        """Test that string input raises TypeError."""
        with pytest.raises(TypeError):
            engine.sqrt("4")

    def test_sqrt_list_raises_typeerror(self, engine):
        """Test that list input raises TypeError."""
        with pytest.raises(TypeError):
            engine.sqrt([4])

    @pytest.mark.parametrize("x,expected", [
        (0, 0.0),
        (1, 1.0),
        (4, 2.0),
        (9, 3.0),
        (16, 4.0),
        (25, 5.0),
        (100, 10.0),
    ])
    def test_sqrt_parametrized_perfect_squares(self, engine, x, expected):
        """Parametrized test for square root of perfect squares."""
        assert engine.sqrt(x) == pytest.approx(expected)
