"""Tests for 12 new scientific operation classes.

Tests the trigonometric (sin, cos, tan, asin, acos, atan), hyperbolic
(sinh, cosh, tanh), exponential (exp), and constant (pi, e) operations
in scientific mode.

These operations were added to support the scientific mode feature in Issue #411.
"""

import math
import pytest
from src.calculator.operations.scientific import (
    ScientificSin,
    ScientificCos,
    ScientificTan,
    ScientificAsin,
    ScientificAcos,
    ScientificAtan,
    ScientificSinh,
    ScientificCosh,
    ScientificTanh,
    ScientificExp,
    ScientificPi,
    ScientificE,
)


# ============================================================================
# A. Trigonometric Functions Tests
# ============================================================================

class TestScientificSin:
    """Tests for ScientificSin operation."""

    @pytest.mark.parametrize("angle,expected", [
        (0, 0),
        (math.pi / 2, 1),
        (math.pi, 0),
        (-math.pi / 2, -1),
        (2 * math.pi, 0),
    ])
    def test_sin_happy_path(self, angle, expected):
        """Test sin() with valid angles.

        Input: Various angles (0, π/2, π, -π/2, 2π)
        Expected: Correct sine values (0, 1, 0, -1, 0)
        """
        op = ScientificSin()
        result = op.execute(angle)
        assert result == pytest.approx(expected, abs=1e-10)

    def test_sin_name(self):
        """Test that sin operation has correct name."""
        op = ScientificSin()
        assert op.name == "sin"

    def test_sin_arity(self):
        """Test that sin operation has arity 1 (unary)."""
        op = ScientificSin()
        assert op.arity == 1


class TestScientificCos:
    """Tests for ScientificCos operation."""

    @pytest.mark.parametrize("angle,expected", [
        (0, 1),
        (math.pi / 2, 0),
        (math.pi, -1),
        (2 * math.pi, 1),
    ])
    def test_cos_happy_path(self, angle, expected):
        """Test cos() with valid angles.

        Input: Various angles (0, π/2, π, 2π)
        Expected: Correct cosine values (1, 0, -1, 1)
        """
        op = ScientificCos()
        result = op.execute(angle)
        assert result == pytest.approx(expected, abs=1e-10)

    def test_cos_name(self):
        """Test that cos operation has correct name."""
        op = ScientificCos()
        assert op.name == "cos"

    def test_cos_arity(self):
        """Test that cos operation has arity 1 (unary)."""
        op = ScientificCos()
        assert op.arity == 1


class TestScientificTan:
    """Tests for ScientificTan operation."""

    @pytest.mark.parametrize("angle,expected", [
        (0, 0),
        (math.pi / 4, 1),
        (math.pi, 0),
        (-math.pi / 4, -1),
    ])
    def test_tan_happy_path(self, angle, expected):
        """Test tan() with valid angles.

        Input: Various angles (0, π/4, π, -π/4)
        Expected: Correct tangent values (0, 1, 0, -1)
        """
        op = ScientificTan()
        result = op.execute(angle)
        assert result == pytest.approx(expected, abs=1e-10)

    def test_tan_name(self):
        """Test that tan operation has correct name."""
        op = ScientificTan()
        assert op.name == "tan"

    def test_tan_arity(self):
        """Test that tan operation has arity 1 (unary)."""
        op = ScientificTan()
        assert op.arity == 1


# ============================================================================
# B. Inverse Trigonometric Tests
# ============================================================================

class TestScientificAsin:
    """Tests for ScientificAsin (arcsine) operation."""

    @pytest.mark.parametrize("value,expected", [
        (0, 0),
        (1, math.pi / 2),
        (-1, -math.pi / 2),
    ])
    def test_asin_happy_path(self, value, expected):
        """Test asin() with valid values in domain [-1, 1].

        Input: asin(0), asin(1), asin(-1)
        Expected: 0, π/2, -π/2
        """
        op = ScientificAsin()
        result = op.execute(value)
        assert result == pytest.approx(expected, abs=1e-10)

    @pytest.mark.parametrize("value", [1.1, -1.1, 2, -2, 100])
    def test_asin_domain_error(self, value):
        """Test asin() raises ValueError for values outside [-1, 1].

        Input: asin(1.1), asin(-1.1), asin(2), asin(-2), asin(100)
        Expected: ValueError with appropriate message
        """
        op = ScientificAsin()
        with pytest.raises(ValueError):
            op.execute(value)

    def test_asin_name(self):
        """Test that asin operation has correct name."""
        op = ScientificAsin()
        assert op.name == "asin"

    def test_asin_arity(self):
        """Test that asin operation has arity 1 (unary)."""
        op = ScientificAsin()
        assert op.arity == 1


class TestScientificAcos:
    """Tests for ScientificAcos (arccosine) operation."""

    @pytest.mark.parametrize("value,expected", [
        (1, 0),
        (0, math.pi / 2),
        (-1, math.pi),
    ])
    def test_acos_happy_path(self, value, expected):
        """Test acos() with valid values in domain [-1, 1].

        Input: acos(1), acos(0), acos(-1)
        Expected: 0, π/2, π
        """
        op = ScientificAcos()
        result = op.execute(value)
        assert result == pytest.approx(expected, abs=1e-10)

    @pytest.mark.parametrize("value", [1.1, -1.1, 2, -2, 100])
    def test_acos_domain_error(self, value):
        """Test acos() raises ValueError for values outside [-1, 1].

        Input: acos(1.1), acos(-1.1), acos(2), acos(-2), acos(100)
        Expected: ValueError with appropriate message
        """
        op = ScientificAcos()
        with pytest.raises(ValueError):
            op.execute(value)

    def test_acos_name(self):
        """Test that acos operation has correct name."""
        op = ScientificAcos()
        assert op.name == "acos"

    def test_acos_arity(self):
        """Test that acos operation has arity 1 (unary)."""
        op = ScientificAcos()
        assert op.arity == 1


class TestScientificAtan:
    """Tests for ScientificAtan (arctangent) operation."""

    @pytest.mark.parametrize("value,expected", [
        (0, 0),
        (1, math.pi / 4),
        (-1, -math.pi / 4),
        (-999999, pytest.approx(-math.pi / 2, abs=0.01)),  # Approaches -π/2
        (999999, pytest.approx(math.pi / 2, abs=0.01)),     # Approaches π/2
    ])
    def test_atan_happy_path(self, value, expected):
        """Test atan() with all real numbers (no domain restriction).

        Input: atan(0), atan(1), atan(-1), atan(±large_number)
        Expected: 0, π/4, -π/4, ±π/2
        """
        op = ScientificAtan()
        result = op.execute(value)
        assert result == pytest.approx(expected, abs=1e-10)

    def test_atan_name(self):
        """Test that atan operation has correct name."""
        op = ScientificAtan()
        assert op.name == "atan"

    def test_atan_arity(self):
        """Test that atan operation has arity 1 (unary)."""
        op = ScientificAtan()
        assert op.arity == 1


# ============================================================================
# C. Hyperbolic Function Tests
# ============================================================================

class TestScientificSinh:
    """Tests for ScientificSinh (hyperbolic sine) operation."""

    @pytest.mark.parametrize("value,expected", [
        (0, 0),
        (1, math.sinh(1)),
        (-1, math.sinh(-1)),
    ])
    def test_sinh_happy_path(self, value, expected):
        """Test sinh() with various values.

        Input: sinh(0), sinh(1), sinh(-1)
        Expected: 0, sinh(1)≈1.175, sinh(-1)≈-1.175
        """
        op = ScientificSinh()
        result = op.execute(value)
        assert result == pytest.approx(expected, abs=1e-10)

    def test_sinh_name(self):
        """Test that sinh operation has correct name."""
        op = ScientificSinh()
        assert op.name == "sinh"

    def test_sinh_arity(self):
        """Test that sinh operation has arity 1 (unary)."""
        op = ScientificSinh()
        assert op.arity == 1


class TestScientificCosh:
    """Tests for ScientificCosh (hyperbolic cosine) operation."""

    @pytest.mark.parametrize("value,expected", [
        (0, 1),
        (1, math.cosh(1)),
        (-1, math.cosh(-1)),
    ])
    def test_cosh_happy_path(self, value, expected):
        """Test cosh() with various values.

        Input: cosh(0), cosh(1), cosh(-1)
        Expected: 1, cosh(1)≈1.543, cosh(-1)≈1.543
        """
        op = ScientificCosh()
        result = op.execute(value)
        # cosh is always positive and >= 1
        assert result >= 1
        assert result == pytest.approx(expected, abs=1e-10)

    def test_cosh_always_positive(self):
        """Test that cosh always returns positive values."""
        op = ScientificCosh()
        assert op.execute(-100) > 0
        assert op.execute(0) > 0
        assert op.execute(100) > 0

    def test_cosh_name(self):
        """Test that cosh operation has correct name."""
        op = ScientificCosh()
        assert op.name == "cosh"

    def test_cosh_arity(self):
        """Test that cosh operation has arity 1 (unary)."""
        op = ScientificCosh()
        assert op.arity == 1


class TestScientificTanh:
    """Tests for ScientificTanh (hyperbolic tangent) operation."""

    @pytest.mark.parametrize("value,expected", [
        (0, 0),
        (1, math.tanh(1)),
        (-1, math.tanh(-1)),
    ])
    def test_tanh_happy_path(self, value, expected):
        """Test tanh() with various values.

        Input: tanh(0), tanh(1), tanh(-1)
        Expected: 0, tanh(1)≈0.761, tanh(-1)≈-0.761
        """
        op = ScientificTanh()
        result = op.execute(value)
        assert result == pytest.approx(expected, abs=1e-10)

    def test_tanh_approaches_one(self):
        """Test that tanh approaches 1 for large positive values."""
        op = ScientificTanh()
        result = op.execute(100)
        assert result > 0.99
        assert result <= 1.0

    def test_tanh_approaches_neg_one(self):
        """Test that tanh approaches -1 for large negative values."""
        op = ScientificTanh()
        result = op.execute(-100)
        assert result < -0.99
        assert result >= -1.0

    def test_tanh_name(self):
        """Test that tanh operation has correct name."""
        op = ScientificTanh()
        assert op.name == "tanh"

    def test_tanh_arity(self):
        """Test that tanh operation has arity 1 (unary)."""
        op = ScientificTanh()
        assert op.arity == 1


# ============================================================================
# D. Exponential and Constants Tests
# ============================================================================

class TestScientificExp:
    """Tests for ScientificExp (exponential function e^x) operation."""

    @pytest.mark.parametrize("value,expected", [
        (0, 1),
        (1, math.e),
        (-1, 1 / math.e),
    ])
    def test_exp_happy_path(self, value, expected):
        """Test exp() with various values.

        Input: exp(0), exp(1), exp(-1)
        Expected: 1, e≈2.718, 1/e≈0.367
        """
        op = ScientificExp()
        result = op.execute(value)
        assert result == pytest.approx(expected, abs=1e-10)

    def test_exp_name(self):
        """Test that exp operation has correct name."""
        op = ScientificExp()
        assert op.name == "exp"

    def test_exp_arity(self):
        """Test that exp operation has arity 1 (unary)."""
        op = ScientificExp()
        assert op.arity == 1


class TestScientificPi:
    """Tests for ScientificPi (constant pi) operation."""

    def test_pi_value(self):
        """Test that pi() returns the mathematical constant π.

        Input: pi()
        Expected: math.pi ≈ 3.141592653589793
        """
        op = ScientificPi()
        result = op.execute()
        assert result == pytest.approx(math.pi, abs=1e-15)

    def test_pi_name(self):
        """Test that pi operation has correct name."""
        op = ScientificPi()
        assert op.name == "pi"

    def test_pi_arity(self):
        """Test that pi operation has arity 0 (constant/nullary)."""
        op = ScientificPi()
        assert op.arity == 0


class TestScientificE:
    """Tests for ScientificE (constant e) operation."""

    def test_e_value(self):
        """Test that e() returns the mathematical constant e.

        Input: e()
        Expected: math.e ≈ 2.718281828459045
        """
        op = ScientificE()
        result = op.execute()
        assert result == pytest.approx(math.e, abs=1e-15)

    def test_e_name(self):
        """Test that e operation has correct name."""
        op = ScientificE()
        assert op.name == "e"

    def test_e_arity(self):
        """Test that e operation has arity 0 (constant/nullary)."""
        op = ScientificE()
        assert op.arity == 0
