"""test_modes_basic.py — tests for BasicOperations class.

Tests cover:
- All four arithmetic operations (add, subtract, multiply, divide) with valid inputs
- Edge cases: negative numbers, zero, floats, large numbers, small numbers
- ZeroDivisionError from divide(x, 0)
- History callback injection and invocation
- get_operations() returns correct mapping
"""

import pytest
from unittest.mock import Mock
from src.modes.basic import BasicOperations


# =============================================================================
# Test get_operations
# =============================================================================


class TestGetOperations:
    """Tests for BasicOperations.get_operations() method."""

    def test_get_operations_returns_dict(self):
        """Test that get_operations() returns a dict."""
        ops = BasicOperations()
        result = ops.get_operations()
        assert isinstance(result, dict)

    def test_get_operations_returns_four_operations(self):
        """Test that get_operations() returns exactly 4 operations."""
        ops = BasicOperations()
        result = ops.get_operations()
        assert len(result) == 4

    def test_get_operations_contains_add(self):
        """Test that get_operations() contains 'add'."""
        ops = BasicOperations()
        result = ops.get_operations()
        assert "add" in result

    def test_get_operations_contains_subtract(self):
        """Test that get_operations() contains 'subtract'."""
        ops = BasicOperations()
        result = ops.get_operations()
        assert "subtract" in result

    def test_get_operations_contains_multiply(self):
        """Test that get_operations() contains 'multiply'."""
        ops = BasicOperations()
        result = ops.get_operations()
        assert "multiply" in result

    def test_get_operations_contains_divide(self):
        """Test that get_operations() contains 'divide'."""
        ops = BasicOperations()
        result = ops.get_operations()
        assert "divide" in result

    def test_get_operations_values_are_callable(self):
        """Test that all values in get_operations() are callable."""
        ops = BasicOperations()
        result = ops.get_operations()
        for fn in result.values():
            assert callable(fn)

    def test_get_operations_returns_bound_methods(self):
        """Test that get_operations() returns bound methods."""
        ops = BasicOperations()
        result = ops.get_operations()
        # Bound methods have __self__ attribute
        assert all(hasattr(fn, "__self__") for fn in result.values())


# =============================================================================
# Test Addition
# =============================================================================


class TestAddition:
    """Tests for BasicOperations.add() method."""

    @pytest.mark.parametrize("a,b,expected", [
        (2, 3, 5),
        (0, 5, 5),
        (5, 0, 5),
        (0, 0, 0),
        (-2, 3, 1),
        (3, -2, 1),
        (-2, -3, -5),
        (1.5, 2.5, 4.0),
        (0.1, 0.2, pytest.approx(0.3)),
        (10**15, 1, 10**15 + 1),
        (1e-10, 1e-10, pytest.approx(2e-10)),
    ])
    def test_add_valid_inputs(self, a, b, expected):
        """Test add with various valid numeric inputs."""
        ops = BasicOperations()
        assert ops.add(a, b) == expected

    @pytest.mark.parametrize("invalid_a,invalid_b", [
        ("10", 2),
        (10, "2"),
        (None, 5),
        (5, None),
        ([10], 2),
        (10, [2]),
        ({}, 5),
        (5, {}),
    ])
    def test_add_non_numeric_inputs_raise_typeerror(self, invalid_a, invalid_b):
        """Test that non-numeric inputs raise TypeError."""
        ops = BasicOperations()
        with pytest.raises(TypeError):
            ops.add(invalid_a, invalid_b)

    def test_add_with_callback_invokes_callback(self):
        """Test that add invokes the record_callback with the result."""
        callback = Mock()
        ops = BasicOperations(record_callback=callback)
        result = ops.add(2, 3)
        assert result == 5
        callback.assert_called_once_with(5)

    def test_add_without_callback_does_not_error(self):
        """Test that add works correctly without a callback."""
        ops = BasicOperations(record_callback=None)
        result = ops.add(2, 3)
        assert result == 5


# =============================================================================
# Test Subtraction
# =============================================================================


class TestSubtraction:
    """Tests for BasicOperations.subtract() method."""

    @pytest.mark.parametrize("a,b,expected", [
        (5, 2, 3),
        (2, 5, -3),
        (5, 0, 5),
        (0, 5, -5),
        (0, 0, 0),
        (-2, 3, -5),
        (3, -2, 5),
        (-2, -3, 1),
        (2.5, 1.5, 1.0),
        (0.3, 0.1, pytest.approx(0.2)),
        (10**15, 1, 10**15 - 1),
        (1e-10, 1e-10, pytest.approx(0, abs=1e-15)),
    ])
    def test_subtract_valid_inputs(self, a, b, expected):
        """Test subtract with various valid numeric inputs."""
        ops = BasicOperations()
        assert ops.subtract(a, b) == expected

    @pytest.mark.parametrize("invalid_a,invalid_b", [
        ("5", 2),
        (5, "2"),
        (None, 5),
        (5, None),
        ([5], 2),
        (5, [2]),
        ({}, 5),
        (5, {}),
    ])
    def test_subtract_non_numeric_inputs_raise_typeerror(self, invalid_a, invalid_b):
        """Test that non-numeric inputs raise TypeError."""
        ops = BasicOperations()
        with pytest.raises(TypeError):
            ops.subtract(invalid_a, invalid_b)

    def test_subtract_with_callback_invokes_callback(self):
        """Test that subtract invokes the record_callback with the result."""
        callback = Mock()
        ops = BasicOperations(record_callback=callback)
        result = ops.subtract(5, 2)
        assert result == 3
        callback.assert_called_once_with(3)

    def test_subtract_without_callback_does_not_error(self):
        """Test that subtract works correctly without a callback."""
        ops = BasicOperations(record_callback=None)
        result = ops.subtract(5, 2)
        assert result == 3


# =============================================================================
# Test Multiplication
# =============================================================================


class TestMultiplication:
    """Tests for BasicOperations.multiply() method."""

    @pytest.mark.parametrize("a,b,expected", [
        (2, 3, 6),
        (0, 5, 0),
        (5, 0, 0),
        (0, 0, 0),
        (-2, 3, -6),
        (3, -2, -6),
        (-2, -3, 6),
        (1.5, 2.0, 3.0),
        (0.5, 0.5, 0.25),
        (10**10, 10**10, 10**20),
        (1e-10, 1e10, pytest.approx(1.0)),
    ])
    def test_multiply_valid_inputs(self, a, b, expected):
        """Test multiply with various valid numeric inputs."""
        ops = BasicOperations()
        assert ops.multiply(a, b) == expected

    @pytest.mark.parametrize("invalid_a,invalid_b", [
        (None, 5),
        (5, None),
        ({}, 5),
        (5, {}),
    ])
    def test_multiply_non_numeric_inputs_raise_typeerror(self, invalid_a, invalid_b):
        """Test that non-numeric inputs (None, dict) raise TypeError."""
        ops = BasicOperations()
        with pytest.raises(TypeError):
            ops.multiply(invalid_a, invalid_b)

    def test_multiply_with_callback_invokes_callback(self):
        """Test that multiply invokes the record_callback with the result."""
        callback = Mock()
        ops = BasicOperations(record_callback=callback)
        result = ops.multiply(2, 3)
        assert result == 6
        callback.assert_called_once_with(6)

    def test_multiply_without_callback_does_not_error(self):
        """Test that multiply works correctly without a callback."""
        ops = BasicOperations(record_callback=None)
        result = ops.multiply(2, 3)
        assert result == 6


# =============================================================================
# Test Division
# =============================================================================


class TestDivision:
    """Tests for BasicOperations.divide() method."""

    @pytest.mark.parametrize("a,b,expected", [
        (10, 2, 5.0),
        (7.5, 2.5, 3.0),
        (-10, 2, -5.0),
        (10, -2, -5.0),
        (-10, -2, 5.0),
        (0, 5, 0.0),
        (1, 3, pytest.approx(0.333333333333333)),
        (10**15, 10**10, 10**5),
        (1e-10, 1e-5, pytest.approx(1e-5)),
    ])
    def test_divide_valid_inputs(self, a, b, expected):
        """Test divide with various valid numeric inputs."""
        ops = BasicOperations()
        assert ops.divide(a, b) == expected

    def test_divide_by_zero_raises_zerodivisionerror(self):
        """Test that divide(x, 0) raises ZeroDivisionError."""
        ops = BasicOperations()
        with pytest.raises(ZeroDivisionError):
            ops.divide(10, 0)

    def test_divide_zero_by_zero_raises_zerodivisionerror(self):
        """Test that divide(0, 0) raises ZeroDivisionError."""
        ops = BasicOperations()
        with pytest.raises(ZeroDivisionError):
            ops.divide(0, 0)

    def test_divide_negative_by_zero_raises_zerodivisionerror(self):
        """Test that divide(-x, 0) raises ZeroDivisionError."""
        ops = BasicOperations()
        with pytest.raises(ZeroDivisionError):
            ops.divide(-10, 0)

    @pytest.mark.parametrize("invalid_a,invalid_b", [
        ("10", 2),
        (10, "2"),
        (None, 5),
        (5, None),
        ([10], 2),
        (10, [2]),
        ({}, 5),
        (5, {}),
    ])
    def test_divide_non_numeric_inputs_raise_typeerror(self, invalid_a, invalid_b):
        """Test that non-numeric inputs raise TypeError."""
        ops = BasicOperations()
        with pytest.raises(TypeError):
            ops.divide(invalid_a, invalid_b)

    def test_divide_with_callback_invokes_callback(self):
        """Test that divide invokes the record_callback with the result."""
        callback = Mock()
        ops = BasicOperations(record_callback=callback)
        result = ops.divide(10, 2)
        assert result == 5.0
        callback.assert_called_once_with(5.0)

    def test_divide_by_zero_does_not_invoke_callback(self):
        """Test that divide by zero does not invoke callback before raising."""
        callback = Mock()
        ops = BasicOperations(record_callback=callback)
        with pytest.raises(ZeroDivisionError):
            ops.divide(10, 0)
        # Callback should not have been called since exception is raised before _record
        callback.assert_not_called()

    def test_divide_without_callback_does_not_error(self):
        """Test that divide works correctly without a callback."""
        ops = BasicOperations(record_callback=None)
        result = ops.divide(10, 2)
        assert result == 5.0

    def test_divide_returns_float(self):
        """Test that divide always returns a float."""
        ops = BasicOperations()
        result = ops.divide(10, 2)
        assert isinstance(result, float)


# =============================================================================
# Test Callback Behavior
# =============================================================================


class TestCallbackBehavior:
    """Tests for callback invocation across all operations."""

    def test_multiple_operations_call_callback_multiple_times(self):
        """Test that multiple operations each invoke the callback once."""
        callback = Mock()
        ops = BasicOperations(record_callback=callback)
        ops.add(1, 2)
        ops.subtract(5, 3)
        ops.multiply(2, 3)
        assert callback.call_count == 3

    def test_callback_receives_result_values(self):
        """Test that callback receives the actual result values."""
        results = []
        ops = BasicOperations(record_callback=lambda r: results.append(r))
        ops.add(2, 3)
        ops.subtract(5, 2)
        ops.multiply(2, 3)
        assert results == [5, 3, 6]

    def test_callback_not_invoked_when_none(self):
        """Test that no callback is invoked when record_callback is None."""
        # This test just verifies that passing None doesn't error
        ops = BasicOperations(record_callback=None)
        ops.add(1, 2)
        ops.subtract(3, 1)
        # No assertion needed; if it doesn't raise, the test passes
        assert True
