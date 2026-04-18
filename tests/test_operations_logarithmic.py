"""Comprehensive tests for logarithmic operations module.

Tests cover base-10 logarithm (log) and natural logarithm (ln) with normal cases,
edge cases, and error conditions.
"""

import pytest
import math
from src.operations import logarithmic


class TestLog:
    """Test suite for logarithmic.log() - base-10 logarithm"""

    def test_log_one(self):
        """log(1) = 0."""
        assert logarithmic.log(1) == 0.0

    def test_log_ten(self):
        """log(10) = 1."""
        result = logarithmic.log(10)
        assert abs(result - 1.0) < 1e-10

    def test_log_hundred(self):
        """log(100) = 2."""
        result = logarithmic.log(100)
        assert abs(result - 2.0) < 1e-10

    def test_log_thousand(self):
        """log(1000) = 3."""
        result = logarithmic.log(1000)
        assert abs(result - 3.0) < 1e-10

    def test_log_positive_integer(self):
        """Happy path: log of positive integers."""
        result = logarithmic.log(5)
        expected = math.log10(5)
        assert abs(result - expected) < 1e-10

    def test_log_positive_float(self):
        """Log of positive float."""
        result = logarithmic.log(2.5)
        expected = math.log10(2.5)
        assert abs(result - expected) < 1e-10

    def test_log_small_positive(self):
        """Log of small positive number (less than 1)."""
        result = logarithmic.log(0.1)
        assert abs(result - (-1.0)) < 1e-10

    def test_log_very_small_positive(self):
        """Log of very small positive number."""
        result = logarithmic.log(0.001)
        assert abs(result - (-3.0)) < 1e-10

    def test_log_between_zero_and_one(self):
        """Log of number between 0 and 1 is negative."""
        result = logarithmic.log(0.5)
        expected = math.log10(0.5)
        assert result < 0
        assert abs(result - expected) < 1e-10

    def test_log_large_number(self):
        """Log of large positive number."""
        result = logarithmic.log(10**10)
        assert abs(result - 10.0) < 1e-10

    def test_log_very_large_number(self):
        """Log of very large positive number."""
        result = logarithmic.log(10**100)
        assert abs(result - 100.0) < 1e-10

    def test_log_zero_raises_error(self):
        """log(0) raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            logarithmic.log(0)
        assert "log requires a positive number" in str(exc_info.value)
        assert "0" in str(exc_info.value)

    def test_log_negative_one_raises_error(self):
        """log(-1) raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            logarithmic.log(-1)
        assert "log requires a positive number" in str(exc_info.value)
        assert "-1" in str(exc_info.value)

    def test_log_negative_number_raises_error(self):
        """log of negative number raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            logarithmic.log(-5)
        assert "log requires a positive number" in str(exc_info.value)

    def test_log_small_negative_raises_error(self):
        """log of small negative number raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            logarithmic.log(-0.001)
        assert "log requires a positive number" in str(exc_info.value)

    def test_log_negative_zero(self):
        """log(-0.0) raises ValueError (negative zero is still <= 0)."""
        with pytest.raises(ValueError) as exc_info:
            logarithmic.log(-0.0)
        assert "log requires a positive number" in str(exc_info.value)

    def test_log_infinity(self):
        """log(infinity) = infinity."""
        result = logarithmic.log(float('inf'))
        assert result == float('inf')

    def test_log_negative_infinity_raises_error(self):
        """log(-infinity) raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            logarithmic.log(float('-inf'))
        assert "log requires a positive number" in str(exc_info.value)

    def test_log_nan_propagates(self):
        """log(NaN) propagates NaN (NaN is not <= 0 in comparison)."""
        result = logarithmic.log(float('nan'))
        assert math.isnan(result)

    def test_log_string_raises_error(self):
        """String input should raise TypeError."""
        with pytest.raises(TypeError):
            logarithmic.log("10")

    def test_log_none_raises_error(self):
        """None input should raise TypeError."""
        with pytest.raises(TypeError):
            logarithmic.log(None)

    def test_log_list_raises_error(self):
        """List input should raise TypeError."""
        with pytest.raises(TypeError):
            logarithmic.log([10])

    def test_log_monotonically_increasing(self):
        """Log is monotonically increasing."""
        assert logarithmic.log(1) < logarithmic.log(10)
        assert logarithmic.log(10) < logarithmic.log(100)

    def test_log_inverse_property(self):
        """10^log(x) = x (approximately)."""
        x = 42
        log_x = logarithmic.log(x)
        result = 10 ** log_x
        assert abs(result - x) < 1e-10


class TestLn:
    """Test suite for logarithmic.ln() - natural logarithm"""

    def test_ln_one(self):
        """ln(1) = 0."""
        assert logarithmic.ln(1) == 0.0

    def test_ln_e(self):
        """ln(e) = 1."""
        result = logarithmic.ln(math.e)
        assert abs(result - 1.0) < 1e-10

    def test_ln_e_squared(self):
        """ln(e^2) = 2."""
        result = logarithmic.ln(math.e ** 2)
        assert abs(result - 2.0) < 1e-10

    def test_ln_positive_integer(self):
        """Happy path: ln of positive integers."""
        result = logarithmic.ln(5)
        expected = math.log(5)
        assert abs(result - expected) < 1e-10

    def test_ln_positive_float(self):
        """Ln of positive float."""
        result = logarithmic.ln(2.5)
        expected = math.log(2.5)
        assert abs(result - expected) < 1e-10

    def test_ln_small_positive(self):
        """Ln of small positive number (less than 1)."""
        result = logarithmic.ln(0.5)
        expected = math.log(0.5)
        assert result < 0
        assert abs(result - expected) < 1e-10

    def test_ln_very_small_positive(self):
        """Ln of very small positive number."""
        result = logarithmic.ln(0.01)
        expected = math.log(0.01)
        assert abs(result - expected) < 1e-10

    def test_ln_between_zero_and_one(self):
        """Ln of number between 0 and 1 is negative."""
        result = logarithmic.ln(0.1)
        expected = math.log(0.1)
        assert result < 0
        assert abs(result - expected) < 1e-10

    def test_ln_large_number(self):
        """Ln of large positive number."""
        result = logarithmic.ln(1000)
        expected = math.log(1000)
        assert abs(result - expected) < 1e-10

    def test_ln_very_large_number(self):
        """Ln of very large positive number."""
        result = logarithmic.ln(10**50)
        expected = math.log(10**50)
        assert abs(result - expected) < 1e-10

    def test_ln_zero_raises_error(self):
        """ln(0) raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            logarithmic.ln(0)
        assert "ln requires a positive number" in str(exc_info.value)
        assert "0" in str(exc_info.value)

    def test_ln_negative_one_raises_error(self):
        """ln(-1) raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            logarithmic.ln(-1)
        assert "ln requires a positive number" in str(exc_info.value)
        assert "-1" in str(exc_info.value)

    def test_ln_negative_number_raises_error(self):
        """ln of negative number raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            logarithmic.ln(-5)
        assert "ln requires a positive number" in str(exc_info.value)

    def test_ln_small_negative_raises_error(self):
        """ln of small negative number raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            logarithmic.ln(-0.001)
        assert "ln requires a positive number" in str(exc_info.value)

    def test_ln_negative_zero(self):
        """ln(-0.0) raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            logarithmic.ln(-0.0)
        assert "ln requires a positive number" in str(exc_info.value)

    def test_ln_infinity(self):
        """ln(infinity) = infinity."""
        result = logarithmic.ln(float('inf'))
        assert result == float('inf')

    def test_ln_negative_infinity_raises_error(self):
        """ln(-infinity) raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            logarithmic.ln(float('-inf'))
        assert "ln requires a positive number" in str(exc_info.value)

    def test_ln_nan_propagates(self):
        """ln(NaN) propagates NaN."""
        result = logarithmic.ln(float('nan'))
        assert math.isnan(result)

    def test_ln_string_raises_error(self):
        """String input should raise TypeError."""
        with pytest.raises(TypeError):
            logarithmic.ln("e")

    def test_ln_none_raises_error(self):
        """None input should raise TypeError."""
        with pytest.raises(TypeError):
            logarithmic.ln(None)

    def test_ln_list_raises_error(self):
        """List input should raise TypeError."""
        with pytest.raises(TypeError):
            logarithmic.ln([math.e])

    def test_ln_monotonically_increasing(self):
        """Ln is monotonically increasing."""
        assert logarithmic.ln(1) < logarithmic.ln(math.e)
        assert logarithmic.ln(math.e) < logarithmic.ln(math.e**2)

    def test_ln_inverse_property(self):
        """e^ln(x) = x (approximately)."""
        x = 42
        ln_x = logarithmic.ln(x)
        result = math.e ** ln_x
        assert abs(result - x) < 1e-10


class TestLogarithmicIntegration:
    """Integration tests combining logarithmic operations."""

    def test_log_and_ln_relationship(self):
        """log(x) = ln(x) / ln(10)."""
        x = 100
        log_x = logarithmic.log(x)
        ln_x = logarithmic.ln(x)
        ln_10 = logarithmic.ln(10)
        expected = ln_x / ln_10
        assert abs(log_x - expected) < 1e-10

    def test_log_and_power_inverse(self):
        """log(10^x) = x."""
        x = 5
        power_result = 10 ** x
        log_result = logarithmic.log(power_result)
        assert abs(log_result - x) < 1e-10

    def test_ln_and_power_inverse(self):
        """ln(e^x) = x."""
        x = 5
        power_result = math.e ** x
        ln_result = logarithmic.ln(power_result)
        assert abs(ln_result - x) < 1e-10

    def test_log_product_rule(self):
        """log(a*b) = log(a) + log(b)."""
        a, b = 5, 20
        result1 = logarithmic.log(a * b)
        result2 = logarithmic.log(a) + logarithmic.log(b)
        assert abs(result1 - result2) < 1e-10

    def test_ln_product_rule(self):
        """ln(a*b) = ln(a) + ln(b)."""
        a, b = 7, 13
        result1 = logarithmic.ln(a * b)
        result2 = logarithmic.ln(a) + logarithmic.ln(b)
        assert abs(result1 - result2) < 1e-10

    def test_log_quotient_rule(self):
        """log(a/b) = log(a) - log(b)."""
        a, b = 100, 10
        result1 = logarithmic.log(a / b)
        result2 = logarithmic.log(a) - logarithmic.log(b)
        assert abs(result1 - result2) < 1e-10

    def test_ln_quotient_rule(self):
        """ln(a/b) = ln(a) - ln(b)."""
        a, b = math.e ** 3, math.e
        result1 = logarithmic.ln(a / b)
        result2 = logarithmic.ln(a) - logarithmic.ln(b)
        assert abs(result1 - result2) < 1e-10

    def test_log_power_rule(self):
        """log(x^n) = n * log(x)."""
        from src.operations import exponents
        x, n = 5, 3
        x_power_n = exponents.power(x, n)
        result1 = logarithmic.log(x_power_n)
        result2 = n * logarithmic.log(x)
        assert abs(result1 - result2) < 1e-10

    def test_ln_power_rule(self):
        """ln(x^n) = n * ln(x)."""
        from src.operations import exponents
        x, n = math.e * 2, 4
        x_power_n = exponents.power(x, n)
        result1 = logarithmic.ln(x_power_n)
        result2 = n * logarithmic.ln(x)
        assert abs(result1 - result2) < 1e-10

    def test_log_of_one_always_zero(self):
        """log(1) always equals 0, independent of base."""
        assert logarithmic.log(1) == 0
        assert logarithmic.ln(1) == 0

    def test_log_domain_restrictions(self):
        """Both log and ln require positive inputs."""
        # Negative inputs
        with pytest.raises(ValueError):
            logarithmic.log(-5)
        with pytest.raises(ValueError):
            logarithmic.ln(-5)

        # Zero
        with pytest.raises(ValueError):
            logarithmic.log(0)
        with pytest.raises(ValueError):
            logarithmic.ln(0)

    def test_log_monotonicity_comparison(self):
        """Both logs are monotonically increasing."""
        values = [0.5, 1, 2, 5, 10, 100]
        log_results = [logarithmic.log(v) for v in values]
        ln_results = [logarithmic.ln(v) for v in values]

        # Each list should be strictly increasing
        for i in range(len(log_results) - 1):
            assert log_results[i] < log_results[i+1]
            assert ln_results[i] < ln_results[i+1]

    def test_change_of_base_formula(self):
        """log_b(x) = ln(x) / ln(b)."""
        # Using log base 2
        x = 8
        log_2_8 = logarithmic.ln(x) / logarithmic.ln(2)
        # log_2(8) should equal 3
        assert abs(log_2_8 - 3.0) < 1e-10
