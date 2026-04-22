"""test_modes_advanced.py — tests for AdvancedOperations class.

Tests cover:
- All eight advanced operations with valid inputs
- Error handling: TypeError for non-integer factorial, ValueError for invalid math domains
- History callback injection and invocation
- get_operations() returns correct mapping
"""

import pytest
import math
from unittest.mock import Mock
from src.modes.advanced import AdvancedOperations


# =============================================================================
# Test get_operations
# =============================================================================


class TestGetOperations:
    """Tests for AdvancedOperations.get_operations() method."""

    def test_get_operations_returns_dict(self):
        """Test that get_operations() returns a dict."""
        ops = AdvancedOperations()
        result = ops.get_operations()
        assert isinstance(result, dict)

    def test_get_operations_returns_eight_operations(self):
        """Test that get_operations() returns exactly 8 operations."""
        ops = AdvancedOperations()
        result = ops.get_operations()
        assert len(result) == 8

    def test_get_operations_contains_all_expected_names(self):
        """Test that get_operations() contains all expected operation names."""
        ops = AdvancedOperations()
        result = ops.get_operations()
        expected_names = {
            "factorial",
            "square",
            "cube",
            "square_root",
            "cube_root",
            "power",
            "natural_log",
            "log_base_10",
        }
        assert set(result.keys()) == expected_names

    def test_get_operations_values_are_callable(self):
        """Test that all values in get_operations() are callable."""
        ops = AdvancedOperations()
        result = ops.get_operations()
        for fn in result.values():
            assert callable(fn)

    def test_get_operations_returns_bound_methods(self):
        """Test that get_operations() returns bound methods."""
        ops = AdvancedOperations()
        result = ops.get_operations()
        assert all(hasattr(fn, "__self__") for fn in result.values())


# =============================================================================
# Test Factorial
# =============================================================================


class TestFactorial:
    """Tests for AdvancedOperations.factorial() method."""

    @pytest.mark.parametrize("n,expected", [
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 6),
        (4, 24),
        (5, 120),
        (10, 3628800),
        (20, 2432902008176640000),
    ])
    def test_factorial_valid_inputs(self, n, expected):
        """Test factorial with valid non-negative integer inputs."""
        ops = AdvancedOperations()
        assert ops.factorial(n) == expected

    def test_factorial_with_float_raises_typeerror(self):
        """Test that factorial(float) raises TypeError."""
        ops = AdvancedOperations()
        with pytest.raises(TypeError):
            ops.factorial(3.5)

    def test_factorial_with_string_raises_typeerror(self):
        """Test that factorial(string) raises TypeError."""
        ops = AdvancedOperations()
        with pytest.raises(TypeError):
            ops.factorial("5")

    def test_factorial_with_none_raises_typeerror(self):
        """Test that factorial(None) raises TypeError."""
        ops = AdvancedOperations()
        with pytest.raises(TypeError):
            ops.factorial(None)

    def test_factorial_with_list_raises_typeerror(self):
        """Test that factorial(list) raises TypeError."""
        ops = AdvancedOperations()
        with pytest.raises(TypeError):
            ops.factorial([5])

    def test_factorial_with_bool_raises_typeerror(self):
        """Test that factorial(bool) raises TypeError (bool is a special case)."""
        ops = AdvancedOperations()
        with pytest.raises(TypeError):
            ops.factorial(True)

    def test_factorial_with_negative_raises_valueerror(self):
        """Test that factorial(-n) raises ValueError."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.factorial(-1)

    def test_factorial_with_large_negative_raises_valueerror(self):
        """Test that factorial(-100) raises ValueError."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.factorial(-100)

    def test_factorial_with_callback_invokes_callback(self):
        """Test that factorial invokes the record_callback with the result."""
        callback = Mock()
        ops = AdvancedOperations(record_callback=callback)
        result = ops.factorial(5)
        assert result == 120
        callback.assert_called_once_with(120)

    def test_factorial_without_callback_does_not_error(self):
        """Test that factorial works correctly without a callback."""
        ops = AdvancedOperations(record_callback=None)
        result = ops.factorial(5)
        assert result == 120


# =============================================================================
# Test Square
# =============================================================================


class TestSquare:
    """Tests for AdvancedOperations.square() method."""

    @pytest.mark.parametrize("x,expected", [
        (0, 0),
        (1, 1),
        (2, 4),
        (3, 9),
        (5, 25),
        (-2, 4),
        (-5, 25),
        (0.5, 0.25),
        (1.5, 2.25),
        (10**10, 10**20),
    ])
    def test_square_valid_inputs(self, x, expected):
        """Test square with various valid numeric inputs."""
        ops = AdvancedOperations()
        assert ops.square(x) == expected

    def test_square_with_callback_invokes_callback(self):
        """Test that square invokes the record_callback with the result."""
        callback = Mock()
        ops = AdvancedOperations(record_callback=callback)
        result = ops.square(3)
        assert result == 9
        callback.assert_called_once_with(9)

    def test_square_without_callback_does_not_error(self):
        """Test that square works correctly without a callback."""
        ops = AdvancedOperations(record_callback=None)
        result = ops.square(3)
        assert result == 9


# =============================================================================
# Test Cube
# =============================================================================


class TestCube:
    """Tests for AdvancedOperations.cube() method."""

    @pytest.mark.parametrize("x,expected", [
        (0, 0),
        (1, 1),
        (2, 8),
        (3, 27),
        (5, 125),
        (-2, -8),
        (-5, -125),
        (0.5, 0.125),
        (10**10, 10**30),
    ])
    def test_cube_valid_inputs(self, x, expected):
        """Test cube with various valid numeric inputs."""
        ops = AdvancedOperations()
        assert ops.cube(x) == expected

    def test_cube_with_callback_invokes_callback(self):
        """Test that cube invokes the record_callback with the result."""
        callback = Mock()
        ops = AdvancedOperations(record_callback=callback)
        result = ops.cube(3)
        assert result == 27
        callback.assert_called_once_with(27)

    def test_cube_without_callback_does_not_error(self):
        """Test that cube works correctly without a callback."""
        ops = AdvancedOperations(record_callback=None)
        result = ops.cube(3)
        assert result == 27


# =============================================================================
# Test Square Root
# =============================================================================


class TestSquareRoot:
    """Tests for AdvancedOperations.square_root() method."""

    @pytest.mark.parametrize("x,expected", [
        (0, 0.0),
        (1, 1.0),
        (4, 2.0),
        (9, 3.0),
        (25, 5.0),
        (0.25, 0.5),
        (2, pytest.approx(1.4142135623730951)),
    ])
    def test_square_root_valid_inputs(self, x, expected):
        """Test square_root with valid non-negative inputs."""
        ops = AdvancedOperations()
        assert ops.square_root(x) == expected

    def test_square_root_negative_raises_valueerror(self):
        """Test that square_root(-n) raises ValueError."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.square_root(-1)

    def test_square_root_large_negative_raises_valueerror(self):
        """Test that square_root(-100) raises ValueError."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.square_root(-100)

    def test_square_root_with_callback_invokes_callback(self):
        """Test that square_root invokes the record_callback with the result."""
        callback = Mock()
        ops = AdvancedOperations(record_callback=callback)
        result = ops.square_root(4)
        assert result == 2.0
        callback.assert_called_once_with(2.0)

    def test_square_root_without_callback_does_not_error(self):
        """Test that square_root works correctly without a callback."""
        ops = AdvancedOperations(record_callback=None)
        result = ops.square_root(4)
        assert result == 2.0


# =============================================================================
# Test Cube Root
# =============================================================================


class TestCubeRoot:
    """Tests for AdvancedOperations.cube_root() method."""

    @pytest.mark.parametrize("x,expected", [
        (0, 0.0),
        (1, 1.0),
        (8, 2.0),
        (27, 3.0),
        (125, 5.0),
        (-8, -2.0),
        (-27, -3.0),
        (-125, -5.0),
        (0.125, 0.5),
    ])
    def test_cube_root_valid_inputs(self, x, expected):
        """Test cube_root with various valid inputs (including negative)."""
        ops = AdvancedOperations()
        result = ops.cube_root(x)
        assert abs(result - expected) < 1e-10 or result == pytest.approx(expected)

    def test_cube_root_negative_numbers_preserve_sign(self):
        """Test that cube_root preserves sign for negative numbers."""
        ops = AdvancedOperations()
        result = ops.cube_root(-8)
        assert result < 0
        assert abs(result - (-2.0)) < 1e-10

    def test_cube_root_with_callback_invokes_callback(self):
        """Test that cube_root invokes the record_callback with the result."""
        callback = Mock()
        ops = AdvancedOperations(record_callback=callback)
        result = ops.cube_root(8)
        assert result == pytest.approx(2.0)
        callback.assert_called_once()
        # Verify callback was called with the result
        assert callback.call_args[0][0] == pytest.approx(2.0)

    def test_cube_root_without_callback_does_not_error(self):
        """Test that cube_root works correctly without a callback."""
        ops = AdvancedOperations(record_callback=None)
        result = ops.cube_root(8)
        assert result == pytest.approx(2.0)


# =============================================================================
# Test Power
# =============================================================================


class TestPower:
    """Tests for AdvancedOperations.power() method."""

    @pytest.mark.parametrize("base,exponent,expected", [
        (2, 0, 1),
        (2, 1, 2),
        (2, 2, 4),
        (2, 3, 8),
        (2, 10, 1024),
        (3, 3, 27),
        (10, 5, 100000),
        (0.5, 2, 0.25),
        (2, -1, 0.5),
        (10, -2, 0.01),
        (-2, 2, 4),
        (-2, 3, -8),
    ])
    def test_power_valid_inputs(self, base, exponent, expected):
        """Test power with various valid inputs."""
        ops = AdvancedOperations()
        result = ops.power(base, exponent)
        assert result == pytest.approx(expected)

    def test_power_with_callback_invokes_callback(self):
        """Test that power invokes the record_callback with the result."""
        callback = Mock()
        ops = AdvancedOperations(record_callback=callback)
        result = ops.power(2, 3)
        assert result == 8
        callback.assert_called_once_with(8)

    def test_power_without_callback_does_not_error(self):
        """Test that power works correctly without a callback."""
        ops = AdvancedOperations(record_callback=None)
        result = ops.power(2, 3)
        assert result == 8


# =============================================================================
# Test Natural Logarithm
# =============================================================================


class TestNaturalLog:
    """Tests for AdvancedOperations.natural_log() method."""

    @pytest.mark.parametrize("x,expected", [
        (1, 0.0),
        (math.e, pytest.approx(1.0)),
        (10, pytest.approx(2.302585092994046)),
        (0.5, pytest.approx(-0.6931471805599453)),
        (100, pytest.approx(4.605170185988092)),
    ])
    def test_natural_log_valid_inputs(self, x, expected):
        """Test natural_log with valid positive inputs."""
        ops = AdvancedOperations()
        result = ops.natural_log(x)
        assert result == expected

    def test_natural_log_zero_raises_valueerror(self):
        """Test that natural_log(0) raises ValueError."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.natural_log(0)

    def test_natural_log_negative_raises_valueerror(self):
        """Test that natural_log(-n) raises ValueError."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.natural_log(-1)

    def test_natural_log_with_callback_invokes_callback(self):
        """Test that natural_log invokes the record_callback with the result."""
        callback = Mock()
        ops = AdvancedOperations(record_callback=callback)
        result = ops.natural_log(1)
        assert result == 0.0
        callback.assert_called_once_with(0.0)

    def test_natural_log_without_callback_does_not_error(self):
        """Test that natural_log works correctly without a callback."""
        ops = AdvancedOperations(record_callback=None)
        result = ops.natural_log(1)
        assert result == 0.0


# =============================================================================
# Test Base-10 Logarithm
# =============================================================================


class TestLogBase10:
    """Tests for AdvancedOperations.log_base_10() method."""

    @pytest.mark.parametrize("x,expected", [
        (1, 0.0),
        (10, 1.0),
        (100, 2.0),
        (1000, 3.0),
        (0.1, pytest.approx(-1.0)),
        (0.01, pytest.approx(-2.0)),
    ])
    def test_log_base_10_valid_inputs(self, x, expected):
        """Test log_base_10 with valid positive inputs."""
        ops = AdvancedOperations()
        result = ops.log_base_10(x)
        assert result == expected

    def test_log_base_10_zero_raises_valueerror(self):
        """Test that log_base_10(0) raises ValueError."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.log_base_10(0)

    def test_log_base_10_negative_raises_valueerror(self):
        """Test that log_base_10(-n) raises ValueError."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.log_base_10(-1)

    def test_log_base_10_with_callback_invokes_callback(self):
        """Test that log_base_10 invokes the record_callback with the result."""
        callback = Mock()
        ops = AdvancedOperations(record_callback=callback)
        result = ops.log_base_10(10)
        assert result == 1.0
        callback.assert_called_once_with(1.0)

    def test_log_base_10_without_callback_does_not_error(self):
        """Test that log_base_10 works correctly without a callback."""
        ops = AdvancedOperations(record_callback=None)
        result = ops.log_base_10(10)
        assert result == 1.0


# =============================================================================
# Test Callback Behavior
# =============================================================================


class TestCallbackBehavior:
    """Tests for callback invocation across all operations."""

    def test_multiple_operations_call_callback_multiple_times(self):
        """Test that multiple operations each invoke the callback once."""
        callback = Mock()
        ops = AdvancedOperations(record_callback=callback)
        ops.square(2)
        ops.cube(2)
        ops.factorial(5)
        assert callback.call_count == 3

    def test_callback_receives_result_values(self):
        """Test that callback receives the actual result values."""
        results = []
        ops = AdvancedOperations(record_callback=lambda r: results.append(r))
        ops.square(2)
        ops.cube(3)
        ops.factorial(3)
        assert results == [4, 27, 6]

    def test_callback_not_invoked_when_none(self):
        """Test that no callback is invoked when record_callback is None."""
        ops = AdvancedOperations(record_callback=None)
        ops.square(2)
        ops.cube(3)
        # No assertion needed; if it doesn't raise, the test passes
        assert True

    def test_factorial_error_does_not_invoke_callback(self):
        """Test that callback is not invoked when factorial raises an error."""
        callback = Mock()
        ops = AdvancedOperations(record_callback=callback)
        with pytest.raises(ValueError):
            ops.factorial(-1)
        callback.assert_not_called()

    def test_square_root_error_does_not_invoke_callback(self):
        """Test that callback is not invoked when square_root raises an error."""
        callback = Mock()
        ops = AdvancedOperations(record_callback=callback)
        with pytest.raises(ValueError):
            ops.square_root(-1)
        callback.assert_not_called()

    def test_natural_log_error_does_not_invoke_callback(self):
        """Test that callback is not invoked when natural_log raises an error."""
        callback = Mock()
        ops = AdvancedOperations(record_callback=callback)
        with pytest.raises(ValueError):
            ops.natural_log(0)
        callback.assert_not_called()
