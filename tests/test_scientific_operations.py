"""test_scientific_operations.py — comprehensive unit tests for ScientificOperations.

Tests cover:
- Trigonometric functions: sin, cos, tan with known values
- Inverse trigonometric functions: asin, acos, atan with domain validation
- Hyperbolic functions: sinh, cosh, tanh
- Angle conversion: degrees, radians
- Exponential/logarithmic: exp, ln with domain validation
- get_operations() returns all 13 operations
- History recording for all operations
"""

import pytest
import math
from src.modes.scientific import ScientificOperations


@pytest.fixture
def scientific_ops():
    """Fixture providing a fresh ScientificOperations instance."""
    return ScientificOperations()


# =============================================================================
# TestTrigonometricOperations - sin, cos, tan
# =============================================================================


class TestSine:
    """Tests for the sin method."""

    @pytest.mark.parametrize("x,expected", [
        (0, 0),
        (math.pi / 2, 1),
        (math.pi, pytest.approx(0, abs=1e-10)),
        (3 * math.pi / 2, -1),
        (2 * math.pi, pytest.approx(0, abs=1e-10)),
        (math.pi / 6, pytest.approx(0.5)),
        (math.pi / 4, pytest.approx(math.sqrt(2) / 2)),
        (-math.pi / 2, -1),
        (-math.pi, pytest.approx(0, abs=1e-10)),
    ])
    def test_sin_known_values(self, scientific_ops, x, expected):
        """Test sin with known mathematical values."""
        result = scientific_ops.sin(x)
        assert result == expected

    def test_sin_matches_math_module(self, scientific_ops):
        """Test that sin results match math.sin."""
        test_values = [0, 0.5, 1, -1, math.pi / 6, math.pi / 2, math.pi]
        for x in test_values:
            assert scientific_ops.sin(x) == pytest.approx(math.sin(x))

    def test_sin_large_angles(self, scientific_ops):
        """Test sin with large angles."""
        # sin is periodic with period 2π
        assert scientific_ops.sin(10 * math.pi) == pytest.approx(0, abs=1e-10)
        assert scientific_ops.sin(10.5 * math.pi) == pytest.approx(math.sin(10.5 * math.pi))


class TestCosine:
    """Tests for the cos method."""

    @pytest.mark.parametrize("x,expected", [
        (0, 1),
        (math.pi / 2, pytest.approx(0, abs=1e-10)),
        (math.pi, -1),
        (3 * math.pi / 2, pytest.approx(0, abs=1e-10)),
        (2 * math.pi, 1),
        (math.pi / 3, pytest.approx(0.5)),
        (math.pi / 4, pytest.approx(math.sqrt(2) / 2)),
        (-math.pi, -1),
    ])
    def test_cos_known_values(self, scientific_ops, x, expected):
        """Test cos with known mathematical values."""
        result = scientific_ops.cos(x)
        assert result == expected

    def test_cos_matches_math_module(self, scientific_ops):
        """Test that cos results match math.cos."""
        test_values = [0, 0.5, 1, -1, math.pi / 6, math.pi / 2, math.pi]
        for x in test_values:
            assert scientific_ops.cos(x) == pytest.approx(math.cos(x))


class TestTangent:
    """Tests for the tan method."""

    @pytest.mark.parametrize("x,expected", [
        (0, 0),
        (math.pi / 4, pytest.approx(1)),
        (math.pi / 6, pytest.approx(1 / math.sqrt(3))),
        (-math.pi / 4, pytest.approx(-1)),
        (math.pi, pytest.approx(0, abs=1e-10)),
    ])
    def test_tan_known_values(self, scientific_ops, x, expected):
        """Test tan with known mathematical values."""
        result = scientific_ops.tan(x)
        assert result == expected

    def test_tan_matches_math_module(self, scientific_ops):
        """Test that tan results match math.tan."""
        test_values = [0, 0.1, -0.1, math.pi / 6, math.pi / 4]
        for x in test_values:
            assert scientific_ops.tan(x) == pytest.approx(math.tan(x))


# =============================================================================
# TestInverseTrigonometricOperations - asin, acos, atan
# =============================================================================


class TestArcSine:
    """Tests for the asin method."""

    @pytest.mark.parametrize("x,expected", [
        (0, 0),
        (1, math.pi / 2),
        (-1, -math.pi / 2),
        (0.5, math.pi / 6),
        (math.sqrt(2) / 2, math.pi / 4),
    ])
    def test_asin_known_values(self, scientific_ops, x, expected):
        """Test asin with known mathematical values."""
        result = scientific_ops.asin(x)
        assert result == pytest.approx(expected)

    def test_asin_valid_domain_bounds(self, scientific_ops):
        """Test asin with valid domain boundary values."""
        # asin domain is [-1, 1]
        assert scientific_ops.asin(-1) == pytest.approx(-math.pi / 2)
        assert scientific_ops.asin(0) == 0
        assert scientific_ops.asin(1) == pytest.approx(math.pi / 2)

    @pytest.mark.parametrize("invalid_x", [1.5, 2, -1.1, -2, 10])
    def test_asin_outside_domain_raises_valueerror(self, scientific_ops, invalid_x):
        """Test that asin outside [-1, 1] raises ValueError."""
        with pytest.raises(ValueError):
            scientific_ops.asin(invalid_x)

    def test_asin_matches_math_module(self, scientific_ops):
        """Test that asin results match math.asin."""
        test_values = [0, 0.5, -0.5, 1, -1, 0.7]
        for x in test_values:
            assert scientific_ops.asin(x) == pytest.approx(math.asin(x))


class TestArcCosine:
    """Tests for the acos method."""

    @pytest.mark.parametrize("x,expected", [
        (0, math.pi / 2),
        (1, 0),
        (-1, math.pi),
        (0.5, math.pi / 3),
        (math.sqrt(2) / 2, math.pi / 4),
    ])
    def test_acos_known_values(self, scientific_ops, x, expected):
        """Test acos with known mathematical values."""
        result = scientific_ops.acos(x)
        assert result == pytest.approx(expected)

    def test_acos_valid_domain_bounds(self, scientific_ops):
        """Test acos with valid domain boundary values."""
        # acos domain is [-1, 1]
        assert scientific_ops.acos(-1) == pytest.approx(math.pi)
        assert scientific_ops.acos(0) == pytest.approx(math.pi / 2)
        assert scientific_ops.acos(1) == 0

    @pytest.mark.parametrize("invalid_x", [1.5, 2, -1.1, -2, 10])
    def test_acos_outside_domain_raises_valueerror(self, scientific_ops, invalid_x):
        """Test that acos outside [-1, 1] raises ValueError."""
        with pytest.raises(ValueError):
            scientific_ops.acos(invalid_x)

    def test_acos_matches_math_module(self, scientific_ops):
        """Test that acos results match math.acos."""
        test_values = [0, 0.5, -0.5, 1, -1, 0.7]
        for x in test_values:
            assert scientific_ops.acos(x) == pytest.approx(math.acos(x))


class TestArcTangent:
    """Tests for the atan method."""

    @pytest.mark.parametrize("x,expected", [
        (0, 0),
        (1, math.pi / 4),
        (-1, -math.pi / 4),
        (math.sqrt(3), math.pi / 3),
        (1 / math.sqrt(3), math.pi / 6),
    ])
    def test_atan_known_values(self, scientific_ops, x, expected):
        """Test atan with known mathematical values."""
        result = scientific_ops.atan(x)
        assert result == pytest.approx(expected)

    def test_atan_no_domain_restriction(self, scientific_ops):
        """Test atan with values outside typical ranges."""
        # atan accepts any real number
        assert isinstance(scientific_ops.atan(1e10), float)
        assert isinstance(scientific_ops.atan(-1e10), float)
        assert isinstance(scientific_ops.atan(1e-10), float)

    def test_atan_matches_math_module(self, scientific_ops):
        """Test that atan results match math.atan."""
        test_values = [0, 0.5, -0.5, 1, -1, 10, -10, 1e10]
        for x in test_values:
            assert scientific_ops.atan(x) == pytest.approx(math.atan(x))


# =============================================================================
# TestHyperbolicOperations - sinh, cosh, tanh
# =============================================================================


class TestHyperbolicSine:
    """Tests for the sinh method."""

    @pytest.mark.parametrize("x,expected", [
        (0, 0),
        (1, pytest.approx(math.sinh(1))),
        (-1, pytest.approx(-math.sinh(1))),
        (math.log(2), 0.75),  # sinh(ln(2)) = 0.75
    ])
    def test_sinh_known_values(self, scientific_ops, x, expected):
        """Test sinh with known mathematical values."""
        result = scientific_ops.sinh(x)
        assert result == pytest.approx(expected)

    def test_sinh_matches_math_module(self, scientific_ops):
        """Test that sinh results match math.sinh."""
        test_values = [0, 0.5, -0.5, 1, -1, 2]
        for x in test_values:
            assert scientific_ops.sinh(x) == pytest.approx(math.sinh(x))


class TestHyperbolicCosine:
    """Tests for the cosh method."""

    @pytest.mark.parametrize("x,expected", [
        (0, 1),
        (1, pytest.approx(math.cosh(1))),
        (-1, pytest.approx(math.cosh(1))),  # cosh is even
    ])
    def test_cosh_known_values(self, scientific_ops, x, expected):
        """Test cosh with known mathematical values."""
        result = scientific_ops.cosh(x)
        assert result == pytest.approx(expected)

    def test_cosh_is_even_function(self, scientific_ops):
        """Test that cosh is an even function: cosh(-x) = cosh(x)."""
        test_values = [0.5, 1, 2, 3]
        for x in test_values:
            assert scientific_ops.cosh(x) == pytest.approx(scientific_ops.cosh(-x))

    def test_cosh_always_positive(self, scientific_ops):
        """Test that cosh is always >= 1."""
        test_values = [-5, -1, 0, 1, 5]
        for x in test_values:
            assert scientific_ops.cosh(x) >= 1

    def test_cosh_matches_math_module(self, scientific_ops):
        """Test that cosh results match math.cosh."""
        test_values = [0, 0.5, -0.5, 1, -1, 2]
        for x in test_values:
            assert scientific_ops.cosh(x) == pytest.approx(math.cosh(x))


class TestHyperbolicTangent:
    """Tests for the tanh method."""

    @pytest.mark.parametrize("x,expected", [
        (0, 0),
        (1, pytest.approx(math.tanh(1))),
        (-1, pytest.approx(-math.tanh(1))),
    ])
    def test_tanh_known_values(self, scientific_ops, x, expected):
        """Test tanh with known mathematical values."""
        result = scientific_ops.tanh(x)
        assert result == pytest.approx(expected)

    def test_tanh_bounded_by_minus_one_and_one(self, scientific_ops):
        """Test that tanh output is always in (-1, 1)."""
        test_values = [-10, -1, 0, 1, 10]
        for x in test_values:
            result = scientific_ops.tanh(x)
            assert -1 < result < 1

    def test_tanh_matches_math_module(self, scientific_ops):
        """Test that tanh results match math.tanh."""
        test_values = [0, 0.5, -0.5, 1, -1, 2]
        for x in test_values:
            assert scientific_ops.tanh(x) == pytest.approx(math.tanh(x))


# =============================================================================
# TestAngleConversion - degrees, radians
# =============================================================================


class TestDegrees:
    """Tests for the degrees method."""

    @pytest.mark.parametrize("radians_val,expected_degrees", [
        (0, 0),
        (math.pi, 180),
        (2 * math.pi, 360),
        (math.pi / 2, 90),
        (math.pi / 6, 30),
        (math.pi / 4, 45),
        (-math.pi, -180),
    ])
    def test_degrees_known_conversions(self, scientific_ops, radians_val, expected_degrees):
        """Test degrees conversion with known values."""
        result = scientific_ops.degrees(radians_val)
        assert result == pytest.approx(expected_degrees)

    def test_degrees_matches_math_module(self, scientific_ops):
        """Test that degrees results match math.degrees."""
        test_values = [0, 1, -1, math.pi, math.pi / 2, 2 * math.pi]
        for x in test_values:
            assert scientific_ops.degrees(x) == pytest.approx(math.degrees(x))


class TestRadians:
    """Tests for the radians method."""

    @pytest.mark.parametrize("degrees_val,expected_radians", [
        (0, 0),
        (180, math.pi),
        (360, 2 * math.pi),
        (90, math.pi / 2),
        (30, math.pi / 6),
        (45, math.pi / 4),
        (-180, -math.pi),
    ])
    def test_radians_known_conversions(self, scientific_ops, degrees_val, expected_radians):
        """Test radians conversion with known values."""
        result = scientific_ops.radians(degrees_val)
        assert result == pytest.approx(expected_radians)

    def test_radians_matches_math_module(self, scientific_ops):
        """Test that radians results match math.radians."""
        test_values = [0, 1, -1, 180, 360, 90]
        for x in test_values:
            assert scientific_ops.radians(x) == pytest.approx(math.radians(x))


# =============================================================================
# TestExponential - exp
# =============================================================================


class TestExponential:
    """Tests for the exp method."""

    @pytest.mark.parametrize("x,expected", [
        (0, 1),
        (1, math.e),
        (2, math.e ** 2),
        (-1, 1 / math.e),
        (math.log(2), 2),
    ])
    def test_exp_known_values(self, scientific_ops, x, expected):
        """Test exp with known mathematical values."""
        result = scientific_ops.exp(x)
        assert result == pytest.approx(expected)

    def test_exp_positive_output(self, scientific_ops):
        """Test that exp always returns positive values."""
        test_values = [-100, -1, 0, 1, 100]
        for x in test_values:
            result = scientific_ops.exp(x)
            assert result > 0

    def test_exp_matches_math_module(self, scientific_ops):
        """Test that exp results match math.exp."""
        test_values = [0, 0.5, -0.5, 1, -1, 2]
        for x in test_values:
            assert scientific_ops.exp(x) == pytest.approx(math.exp(x))


# =============================================================================
# TestLogarithmic - ln
# =============================================================================


class TestNaturalLogarithm:
    """Tests for the ln method."""

    @pytest.mark.parametrize("x,expected", [
        (1, 0),
        (math.e, 1),
        (math.e ** 2, 2),
        (2, pytest.approx(math.log(2))),
        (0.5, pytest.approx(math.log(0.5))),
    ])
    def test_ln_known_values(self, scientific_ops, x, expected):
        """Test ln with known mathematical values."""
        result = scientific_ops.ln(x)
        assert result == pytest.approx(expected)

    @pytest.mark.parametrize("invalid_x", [0, -1, -0.5, -100])
    def test_ln_non_positive_raises_valueerror(self, scientific_ops, invalid_x):
        """Test that ln of non-positive numbers raises ValueError."""
        with pytest.raises(ValueError):
            scientific_ops.ln(invalid_x)

    def test_ln_positive_input_required(self, scientific_ops):
        """Test ln with various positive inputs."""
        # ln is only defined for x > 0
        assert isinstance(scientific_ops.ln(1e-10), float)
        assert isinstance(scientific_ops.ln(1e10), float)
        assert scientific_ops.ln(1e-10) < 0
        assert scientific_ops.ln(1e10) > 0

    def test_ln_matches_math_module(self, scientific_ops):
        """Test that ln results match math.log (which is ln)."""
        test_values = [1, 2, 0.5, math.e, 10]
        for x in test_values:
            assert scientific_ops.ln(x) == pytest.approx(math.log(x))


# =============================================================================
# TestGetOperations
# =============================================================================


class TestGetOperations:
    """Tests for the get_operations method."""

    def test_get_operations_returns_dict(self, scientific_ops):
        """Test that get_operations returns a dictionary."""
        ops = scientific_ops.get_operations()
        assert isinstance(ops, dict)

    def test_get_operations_has_thirteen_operations(self, scientific_ops):
        """Test that get_operations returns 13 operations."""
        ops = scientific_ops.get_operations()
        assert len(ops) == 13

    def test_get_operations_contains_all_trig_functions(self, scientific_ops):
        """Test that all trigonometric functions are present."""
        ops = scientific_ops.get_operations()
        trig_ops = {"sin", "cos", "tan", "asin", "acos", "atan"}
        assert trig_ops.issubset(ops.keys())

    def test_get_operations_contains_all_hyperbolic_functions(self, scientific_ops):
        """Test that all hyperbolic functions are present."""
        ops = scientific_ops.get_operations()
        hyperbolic_ops = {"sinh", "cosh", "tanh"}
        assert hyperbolic_ops.issubset(ops.keys())

    def test_get_operations_contains_angle_conversions(self, scientific_ops):
        """Test that angle conversion functions are present."""
        ops = scientific_ops.get_operations()
        angle_ops = {"degrees", "radians"}
        assert angle_ops.issubset(ops.keys())

    def test_get_operations_contains_exponential_logarithmic(self, scientific_ops):
        """Test that exp and ln are present."""
        ops = scientific_ops.get_operations()
        exp_log_ops = {"exp", "ln"}
        assert exp_log_ops.issubset(ops.keys())

    def test_get_operations_keys_are_strings(self, scientific_ops):
        """Test that all keys in get_operations are strings."""
        ops = scientific_ops.get_operations()
        for key in ops.keys():
            assert isinstance(key, str)

    def test_get_operations_values_are_callables(self, scientific_ops):
        """Test that all values in get_operations are callable."""
        ops = scientific_ops.get_operations()
        for value in ops.values():
            assert callable(value)

    def test_get_operations_expected_names(self, scientific_ops):
        """Test that get_operations contains exactly the expected 13 operation names."""
        ops = scientific_ops.get_operations()
        expected_names = {
            "sin", "cos", "tan",
            "asin", "acos", "atan",
            "sinh", "cosh", "tanh",
            "degrees", "radians",
            "exp", "ln",
        }
        assert set(ops.keys()) == expected_names


# =============================================================================
# TestHistoryRecording
# =============================================================================


class TestHistoryRecording:
    """Tests for history recording via callback."""

    def test_sin_records_via_callback(self):
        """Test that sin records result via callback."""
        recorded_results = []
        def record_callback(result):
            recorded_results.append(result)

        ops = ScientificOperations(record_callback=record_callback)
        result = ops.sin(math.pi / 2)
        assert len(recorded_results) == 1
        assert recorded_results[0] == pytest.approx(1)

    def test_ln_records_via_callback(self):
        """Test that ln records result via callback."""
        recorded_results = []
        def record_callback(result):
            recorded_results.append(result)

        ops = ScientificOperations(record_callback=record_callback)
        result = ops.ln(math.e)
        assert len(recorded_results) == 1
        assert recorded_results[0] == pytest.approx(1)

    def test_asin_out_of_range_does_not_record(self):
        """Test that asin with invalid input does not record via callback."""
        recorded_results = []
        def record_callback(result):
            recorded_results.append(result)

        ops = ScientificOperations(record_callback=record_callback)
        with pytest.raises(ValueError):
            ops.asin(2)
        # Should not have recorded anything
        assert len(recorded_results) == 0

    def test_multiple_operations_recorded_in_order(self):
        """Test that multiple operations are recorded in order."""
        recorded_results = []
        def record_callback(result):
            recorded_results.append(result)

        ops = ScientificOperations(record_callback=record_callback)
        ops.sin(0)
        ops.cos(0)
        ops.exp(0)

        assert len(recorded_results) == 3
        assert recorded_results[0] == 0  # sin(0)
        assert recorded_results[1] == 1  # cos(0)
        assert recorded_results[2] == 1  # exp(0)


# =============================================================================
# TestEdgeCases
# =============================================================================


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_sin_very_large_angle(self, scientific_ops):
        """Test sin with very large angle."""
        result = scientific_ops.sin(1e10)
        assert isinstance(result, float)
        assert -1 <= result <= 1

    def test_cos_very_large_angle(self, scientific_ops):
        """Test cos with very large angle."""
        result = scientific_ops.cos(1e10)
        assert isinstance(result, float)
        assert -1 <= result <= 1

    def test_exp_very_large_exponent_might_overflow(self, scientific_ops):
        """Test exp with large exponent (may result in overflow)."""
        # exp(1000) overflows in Python, let's test with a smaller value
        result = scientific_ops.exp(700)  # Just below the overflow threshold
        assert isinstance(result, float) and result > 0

    def test_exp_very_small_exponent(self, scientific_ops):
        """Test exp with very small exponent."""
        result = scientific_ops.exp(-1000)
        assert result == pytest.approx(0, abs=1e-300)

    def test_ln_very_small_positive_value(self, scientific_ops):
        """Test ln with very small positive value."""
        result = scientific_ops.ln(1e-100)
        assert result < 0
        assert isinstance(result, float)

    def test_ln_very_large_value(self, scientific_ops):
        """Test ln with very large value."""
        result = scientific_ops.ln(1e100)
        assert result > 0
        assert isinstance(result, float)
