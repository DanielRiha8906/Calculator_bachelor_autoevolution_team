"""Comprehensive tests for calculator mode management.

Tests cover:
- get_mode() returns "normal" by default
- set_mode("scientific") succeeds and get_mode() returns "scientific"
- set_mode("normal") works
- set_mode("invalid") raises ValueError
- Mode persists across operations
"""

import pytest
from src.logic import Calculator


@pytest.fixture
def calculator():
    """Provides a fresh Calculator instance for each test."""
    return Calculator()


# ============================================================================
# GET MODE TESTS
# ============================================================================

class TestGetMode:
    """Test suite for Calculator.get_mode method."""

    def test_get_mode_default_is_normal(self, calculator):
        """Test that get_mode returns 'normal' by default."""
        assert calculator.get_mode() == "normal"

    def test_get_mode_returns_string(self, calculator):
        """Test that get_mode returns a string."""
        mode = calculator.get_mode()
        assert isinstance(mode, str)

    def test_get_mode_multiple_calls_consistent(self, calculator):
        """Test that multiple calls to get_mode return the same value."""
        mode1 = calculator.get_mode()
        mode2 = calculator.get_mode()
        mode3 = calculator.get_mode()

        assert mode1 == mode2 == mode3 == "normal"


# ============================================================================
# SET MODE TO SCIENTIFIC TESTS
# ============================================================================

class TestSetModeScientific:
    """Test suite for setting mode to 'scientific'."""

    def test_set_mode_scientific_succeeds(self, calculator):
        """Test that set_mode('scientific') succeeds."""
        calculator.set_mode("scientific")
        # No exception should be raised

    def test_set_mode_scientific_and_get_returns_scientific(self, calculator):
        """Test that set_mode('scientific') makes get_mode return 'scientific'."""
        calculator.set_mode("scientific")
        assert calculator.get_mode() == "scientific"

    def test_set_mode_scientific_from_normal(self, calculator):
        """Test transitioning from normal to scientific mode."""
        assert calculator.get_mode() == "normal"
        calculator.set_mode("scientific")
        assert calculator.get_mode() == "scientific"

    def test_set_mode_scientific_multiple_times(self, calculator):
        """Test setting to scientific mode multiple times."""
        calculator.set_mode("scientific")
        assert calculator.get_mode() == "scientific"

        calculator.set_mode("scientific")
        assert calculator.get_mode() == "scientific"

    def test_set_mode_scientific_case_sensitive(self, calculator):
        """Test that mode setting is case-sensitive."""
        with pytest.raises(ValueError):
            calculator.set_mode("Scientific")

        with pytest.raises(ValueError):
            calculator.set_mode("SCIENTIFIC")


# ============================================================================
# SET MODE TO NORMAL TESTS
# ============================================================================

class TestSetModeNormal:
    """Test suite for setting mode to 'normal'."""

    def test_set_mode_normal_succeeds(self, calculator):
        """Test that set_mode('normal') succeeds."""
        calculator.set_mode("normal")
        # No exception should be raised

    def test_set_mode_normal_and_get_returns_normal(self, calculator):
        """Test that set_mode('normal') makes get_mode return 'normal'."""
        calculator.set_mode("normal")
        assert calculator.get_mode() == "normal"

    def test_set_mode_normal_from_scientific(self, calculator):
        """Test transitioning from scientific back to normal mode."""
        calculator.set_mode("scientific")
        assert calculator.get_mode() == "scientific"

        calculator.set_mode("normal")
        assert calculator.get_mode() == "normal"

    def test_set_mode_normal_multiple_times(self, calculator):
        """Test setting to normal mode multiple times."""
        calculator.set_mode("normal")
        assert calculator.get_mode() == "normal"

        calculator.set_mode("normal")
        assert calculator.get_mode() == "normal"

    def test_set_mode_normal_case_sensitive(self, calculator):
        """Test that mode 'normal' is case-sensitive."""
        with pytest.raises(ValueError):
            calculator.set_mode("Normal")

        with pytest.raises(ValueError):
            calculator.set_mode("NORMAL")


# ============================================================================
# INVALID MODE TESTS
# ============================================================================

class TestSetModeInvalid:
    """Test suite for invalid mode settings."""

    def test_set_mode_invalid_string_raises_valueerror(self, calculator):
        """Test that set_mode with invalid string raises ValueError."""
        with pytest.raises(ValueError):
            calculator.set_mode("invalid")

    def test_set_mode_empty_string_raises_valueerror(self, calculator):
        """Test that set_mode with empty string raises ValueError."""
        with pytest.raises(ValueError):
            calculator.set_mode("")

    def test_set_mode_whitespace_raises_valueerror(self, calculator):
        """Test that set_mode with whitespace raises ValueError."""
        with pytest.raises(ValueError):
            calculator.set_mode("   ")

    def test_set_mode_scientific_with_spaces_raises_valueerror(self, calculator):
        """Test that set_mode with 'scientific ' (with space) raises ValueError."""
        with pytest.raises(ValueError):
            calculator.set_mode("scientific ")

        with pytest.raises(ValueError):
            calculator.set_mode(" scientific")

    def test_set_mode_normal_with_spaces_raises_valueerror(self, calculator):
        """Test that set_mode with 'normal ' (with space) raises ValueError."""
        with pytest.raises(ValueError):
            calculator.set_mode("normal ")

        with pytest.raises(ValueError):
            calculator.set_mode(" normal")

    def test_set_mode_random_string_raises_valueerror(self, calculator):
        """Test that set_mode with random string raises ValueError."""
        with pytest.raises(ValueError):
            calculator.set_mode("xyz")

        with pytest.raises(ValueError):
            calculator.set_mode("calculator")

    def test_set_mode_partial_match_raises_valueerror(self, calculator):
        """Test that set_mode with partial matches raises ValueError."""
        with pytest.raises(ValueError):
            calculator.set_mode("sci")

        with pytest.raises(ValueError):
            calculator.set_mode("norm")

    def test_set_mode_none_raises_valueerror(self, calculator):
        """Test that set_mode with None raises ValueError or TypeError."""
        # The implementation will raise ValueError because None is not a string in the set
        with pytest.raises((ValueError, TypeError)):
            calculator.set_mode(None)

    def test_set_mode_number_raises_valueerror(self, calculator):
        """Test that set_mode with number raises ValueError or TypeError."""
        with pytest.raises((ValueError, TypeError)):
            calculator.set_mode(1)

        with pytest.raises((ValueError, TypeError)):
            calculator.set_mode(0)

    def test_invalid_mode_does_not_change_state(self, calculator):
        """Test that invalid set_mode call does not change the mode."""
        original_mode = calculator.get_mode()
        try:
            calculator.set_mode("invalid")
        except ValueError:
            pass

        assert calculator.get_mode() == original_mode


# ============================================================================
# MODE TOGGLE TESTS
# ============================================================================

class TestModeToggle:
    """Test suite for toggling between modes."""

    def test_toggle_from_normal_to_scientific(self, calculator):
        """Test toggling from normal to scientific."""
        assert calculator.get_mode() == "normal"
        calculator.set_mode("scientific")
        assert calculator.get_mode() == "scientific"

    def test_toggle_from_scientific_to_normal(self, calculator):
        """Test toggling from scientific back to normal."""
        calculator.set_mode("scientific")
        assert calculator.get_mode() == "scientific"
        calculator.set_mode("normal")
        assert calculator.get_mode() == "normal"

    def test_multiple_toggles(self, calculator):
        """Test multiple toggles between modes."""
        modes = ["normal", "scientific", "normal", "scientific", "scientific", "normal"]
        for mode in modes:
            calculator.set_mode(mode)
            assert calculator.get_mode() == mode

    def test_toggle_with_operations_between(self, calculator):
        """Test toggling modes with operations between toggles."""
        calculator.set_mode("normal")
        calculator.add(1, 2)

        calculator.set_mode("scientific")
        assert calculator.get_mode() == "scientific"
        calculator.sin(0)

        calculator.set_mode("normal")
        assert calculator.get_mode() == "normal"
        calculator.multiply(3, 4)


# ============================================================================
# MODE PERSISTENCE TESTS
# ============================================================================

class TestModePersistence:
    """Test suite for mode persistence across operations."""

    def test_mode_persists_after_add_operation(self, calculator):
        """Test that mode persists after add operation."""
        calculator.set_mode("scientific")
        calculator.add(1, 2)
        assert calculator.get_mode() == "scientific"

    def test_mode_persists_after_scientific_operation(self, calculator):
        """Test that mode persists after scientific operation."""
        calculator.set_mode("scientific")
        calculator.sin(0)
        assert calculator.get_mode() == "scientific"

    def test_mode_persists_after_multiple_operations(self, calculator):
        """Test that mode persists after multiple operations."""
        calculator.set_mode("scientific")
        calculator.add(1, 2)
        calculator.sin(0)
        calculator.multiply(3, 4)
        assert calculator.get_mode() == "scientific"

    def test_mode_persists_after_error_operation(self, calculator):
        """Test that mode persists after an operation that raises error."""
        calculator.set_mode("scientific")
        try:
            calculator.sqrt(-1)  # This will raise ValueError
        except ValueError:
            pass

        assert calculator.get_mode() == "scientific"

    def test_mode_independent_from_history(self, calculator):
        """Test that mode is independent from operation history."""
        calculator.set_mode("scientific")
        calculator.add(1, 2)
        calculator.clear_history()

        # Mode should still be scientific after clearing history
        assert calculator.get_mode() == "scientific"

    def test_mode_in_different_instances(self):
        """Test that mode is independent between calculator instances."""
        calc1 = Calculator()
        calc2 = Calculator()

        calc1.set_mode("scientific")
        assert calc1.get_mode() == "scientific"
        assert calc2.get_mode() == "normal"

    def test_mode_set_before_first_operation(self, calculator):
        """Test setting mode before any operation."""
        calculator.set_mode("scientific")
        calculator.sin(0)
        history = calculator.get_history()

        assert len(history) == 1
        assert calculator.get_mode() == "scientific"

    def test_mode_during_history_accumulation(self, calculator):
        """Test that mode persists correctly during history accumulation."""
        calculator.set_mode("scientific")
        calculator.sin(0)
        calculator.cos(0)
        calculator.exp(1)

        history = calculator.get_history()
        assert len(history) == 3
        assert calculator.get_mode() == "scientific"

        # Change mode and add more operations
        calculator.set_mode("normal")
        calculator.add(1, 2)

        history = calculator.get_history()
        assert len(history) == 4
        assert calculator.get_mode() == "normal"


# ============================================================================
# EDGE CASES AND INTEGRATION
# ============================================================================

class TestModeEdgeCases:
    """Test edge cases and integration scenarios."""

    def test_mode_set_repeated_to_same_value(self, calculator):
        """Test setting mode repeatedly to the same value."""
        for _ in range(10):
            calculator.set_mode("scientific")
            assert calculator.get_mode() == "scientific"

    def test_get_mode_does_not_modify_state(self, calculator):
        """Test that calling get_mode doesn't modify internal state."""
        original_mode = "normal"
        for _ in range(100):
            assert calculator.get_mode() == original_mode

    def test_mode_with_all_basic_operations(self, calculator):
        """Test that mode persists through all basic operations."""
        calculator.set_mode("scientific")
        calculator.add(1, 2)
        calculator.subtract(5, 3)
        calculator.multiply(2, 3)
        calculator.divide(10, 2)
        calculator.square(4)
        calculator.cube(3)

        assert calculator.get_mode() == "scientific"

    def test_mode_with_all_scientific_operations(self, calculator):
        """Test that mode persists through all scientific operations."""
        calculator.set_mode("scientific")
        calculator.sin(0)
        calculator.cos(0)
        calculator.tan(0.5)
        calculator.exp(1)
        calculator.log(1)
        calculator.sqrt(4)

        assert calculator.get_mode() == "scientific"
