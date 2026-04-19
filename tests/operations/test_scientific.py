"""Tests for scientific operation functions from src.operations.scientific."""

import math
import pytest
from src.operations.scientific import power, logarithm, natural_logarithm


class TestPowerFunction:
    """Test the power pure function."""

    def test_power_basic(self):
        """Test basic power operation."""
        assert power(2, 3) == 8

    def test_power_zero_exponent(self):
        """Test raising to power of zero."""
        assert power(5, 0) == 1

    def test_power_one_exponent(self):
        """Test raising to power of one."""
        assert power(5, 1) == 5

    def test_power_negative_exponent(self):
        """Test raising to negative exponent."""
        assert power(2, -2) == 0.25

    def test_power_fractional_exponent(self):
        """Test raising to fractional exponent."""
        assert power(4, 0.5) == pytest.approx(2.0)

    def test_power_zero_base_positive_exponent(self):
        """Test raising zero to positive power."""
        assert power(0, 5) == 0

    def test_power_zero_base_zero_exponent(self):
        """Test 0^0."""
        # Python evaluates 0**0 as 1
        assert power(0, 0) == 1

    def test_power_one_base(self):
        """Test raising one to any power."""
        assert power(1, 100) == 1

    def test_power_negative_base_even_exponent(self):
        """Test negative base with even exponent."""
        assert power(-2, 2) == 4

    def test_power_negative_base_odd_exponent(self):
        """Test negative base with odd exponent."""
        assert power(-2, 3) == -8

    def test_power_large_exponent(self):
        """Test large exponent."""
        result = power(2, 10)
        assert result == 1024

    def test_power_fractional_base_fractional_exponent(self):
        """Test fractional base with fractional exponent."""
        result = power(0.25, 0.5)
        assert result == pytest.approx(0.5)

    def test_power_negative_fractional_exponent(self):
        """Test negative fractional exponent."""
        result = power(16, -0.5)
        assert result == pytest.approx(0.25)

    def test_power_very_large_base_small_exponent(self):
        """Test very large base with small exponent."""
        result = power(1e10, 2)
        assert result == 1e20

    def test_power_small_base_large_exponent(self):
        """Test small base with large exponent."""
        result = power(1.5, 10)
        assert result > 0

    def test_power_e_to_one(self):
        """Test e raised to 1."""
        result = power(math.e, 1)
        assert result == pytest.approx(math.e)


class TestLogarithmFunction:
    """Test the logarithm (base-10) pure function."""

    def test_logarithm_basic(self):
        """Test basic base-10 logarithm."""
        assert logarithm(10) == 1.0

    def test_logarithm_100(self):
        """Test log10(100)."""
        assert logarithm(100) == 2.0

    def test_logarithm_1(self):
        """Test log10(1)."""
        assert logarithm(1) == 0.0

    def test_logarithm_fractional(self):
        """Test log10 of fractional value."""
        result = logarithm(0.1)
        assert result == pytest.approx(-1.0)

    def test_logarithm_small_positive(self):
        """Test logarithm of small positive number."""
        result = logarithm(0.001)
        assert result == pytest.approx(-3.0)

    def test_logarithm_very_small_positive(self):
        """Test logarithm of very small positive number."""
        result = logarithm(1e-10)
        assert result == pytest.approx(-10.0)

    def test_logarithm_large_number(self):
        """Test logarithm of large number."""
        result = logarithm(1e20)
        assert result == pytest.approx(20.0)

    def test_logarithm_zero_raises_error(self):
        """Test that log10(0) raises ValueError."""
        with pytest.raises(ValueError, match="not defined for non-positive values"):
            logarithm(0)

    def test_logarithm_negative_raises_error(self):
        """Test that log10(negative) raises ValueError."""
        with pytest.raises(ValueError, match="not defined for non-positive values"):
            logarithm(-5)

    def test_logarithm_very_large_negative_raises_error(self):
        """Test that large negative number raises error."""
        with pytest.raises(ValueError):
            logarithm(-1e10)

    def test_logarithm_2(self):
        """Test log10(2)."""
        result = logarithm(2)
        assert result == pytest.approx(0.301, abs=1e-3)

    def test_logarithm_sqrt_10(self):
        """Test log10(sqrt(10))."""
        result = logarithm(math.sqrt(10))
        assert result == pytest.approx(0.5)

    def test_logarithm_property_additivity(self):
        """Test logarithm property: log(a*b) = log(a) + log(b)."""
        log_2 = logarithm(2)
        log_5 = logarithm(5)
        log_10 = logarithm(10)
        assert log_2 + log_5 == pytest.approx(log_10)


class TestNaturalLogarithmFunction:
    """Test the natural logarithm (base e) pure function."""

    def test_natural_logarithm_e(self):
        """Test ln(e)."""
        assert natural_logarithm(math.e) == pytest.approx(1.0)

    def test_natural_logarithm_1(self):
        """Test ln(1)."""
        assert natural_logarithm(1) == 0.0

    def test_natural_logarithm_e_squared(self):
        """Test ln(e^2)."""
        result = natural_logarithm(math.e ** 2)
        assert result == pytest.approx(2.0)

    def test_natural_logarithm_fractional(self):
        """Test ln of fractional value."""
        result = natural_logarithm(1 / math.e)
        assert result == pytest.approx(-1.0)

    def test_natural_logarithm_small_positive(self):
        """Test ln of small positive number."""
        result = natural_logarithm(0.001)
        assert result < 0

    def test_natural_logarithm_very_small_positive(self):
        """Test ln of very small positive number."""
        result = natural_logarithm(1e-10)
        assert result == pytest.approx(math.log(1e-10))

    def test_natural_logarithm_large_number(self):
        """Test ln of large number."""
        result = natural_logarithm(1e20)
        assert result == pytest.approx(math.log(1e20))

    def test_natural_logarithm_zero_raises_error(self):
        """Test that ln(0) raises ValueError."""
        with pytest.raises(ValueError, match="not defined for non-positive values"):
            natural_logarithm(0)

    def test_natural_logarithm_negative_raises_error(self):
        """Test that ln(negative) raises ValueError."""
        with pytest.raises(ValueError, match="not defined for non-positive values"):
            natural_logarithm(-5)

    def test_natural_logarithm_very_large_negative_raises_error(self):
        """Test that large negative number raises error."""
        with pytest.raises(ValueError):
            natural_logarithm(-1e10)

    def test_natural_logarithm_2(self):
        """Test ln(2)."""
        result = natural_logarithm(2)
        assert result == pytest.approx(0.693, abs=1e-3)

    def test_natural_logarithm_sqrt_e(self):
        """Test ln(sqrt(e))."""
        result = natural_logarithm(math.sqrt(math.e))
        assert result == pytest.approx(0.5)

    def test_natural_logarithm_property_additivity(self):
        """Test logarithm property: ln(a*b) = ln(a) + ln(b)."""
        ln_2 = natural_logarithm(2)
        ln_3 = natural_logarithm(3)
        ln_6 = natural_logarithm(6)
        assert ln_2 + ln_3 == pytest.approx(ln_6)


class TestScientificEdgeCases:
    """Test edge cases for scientific functions."""

    def test_power_associativity_not_applicable(self):
        """Test that power is not associative."""
        # (2^3)^2 = 8^2 = 64
        assert power(power(2, 3), 2) == 64
        # 2^(3^2) = 2^9 = 512
        assert power(2, power(3, 2)) == 512

    def test_logarithm_vs_natural_logarithm(self):
        """Test relationship between log10 and ln."""
        value = 100
        log10_result = logarithm(value)
        ln_result = natural_logarithm(value)
        # log10(x) = ln(x) / ln(10)
        assert log10_result == pytest.approx(ln_result / natural_logarithm(10))

    def test_power_and_logarithm_inverse(self):
        """Test that power and logarithm are inverse operations."""
        base = 10
        value = 5
        # 10^log10(5) should equal 5
        result = power(base, logarithm(value))
        assert result == pytest.approx(value)

    def test_power_and_natural_logarithm_inverse(self):
        """Test that power and natural logarithm are inverse operations."""
        base = math.e
        value = 7
        # e^ln(7) should equal 7
        result = power(base, natural_logarithm(value))
        assert result == pytest.approx(value)

    def test_logarithm_of_power(self):
        """Test logarithm of a power: log(a^b) = b*log(a)."""
        a = 5
        b = 3
        result = logarithm(power(a, b))
        expected = b * logarithm(a)
        assert result == pytest.approx(expected)

    def test_natural_logarithm_of_power(self):
        """Test natural logarithm of a power: ln(a^b) = b*ln(a)."""
        a = 5
        b = 3
        result = natural_logarithm(power(a, b))
        expected = b * natural_logarithm(a)
        assert result == pytest.approx(expected)

    def test_power_with_infinity(self):
        """Test power with infinity."""
        inf = float('inf')
        assert power(2, inf) == inf
        assert power(0.5, inf) == 0

    def test_power_with_nan(self):
        """Test power with NaN."""
        nan = float('nan')
        result = power(2, nan)
        assert result != result  # NaN != NaN

    def test_logarithm_with_very_close_to_zero(self):
        """Test logarithm with value very close to zero."""
        result = logarithm(1e-100)
        assert result == pytest.approx(-100.0)

    def test_natural_logarithm_with_very_close_to_zero(self):
        """Test natural logarithm with value very close to zero."""
        result = natural_logarithm(1e-100)
        assert result == pytest.approx(math.log(1e-100))
