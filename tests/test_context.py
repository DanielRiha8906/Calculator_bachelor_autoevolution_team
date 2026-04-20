"""Comprehensive tests for CalculatorContext.

Tests cover:
- Initialization and default mode
- set_mode() with valid inputs
- set_mode() with invalid inputs
- get_mode() accessor
- is_scientific_mode() predicate
- Mode persistence across multiple calls
- Edge cases with special characters and whitespace
"""

import pytest
from src.context import CalculatorContext


class TestContextInitialization:
    """Test CalculatorContext initialization."""

    def test_context_initial_mode_normal(self):
        """Verify that CalculatorContext initializes with normal mode."""
        context = CalculatorContext()
        assert context.current_mode == "normal"

    def test_context_has_current_mode_attribute(self):
        """Verify that context has current_mode attribute."""
        context = CalculatorContext()
        assert hasattr(context, "current_mode")
        assert isinstance(context.current_mode, str)

    def test_multiple_contexts_independent(self):
        """Verify that multiple contexts are independent."""
        context1 = CalculatorContext()
        context2 = CalculatorContext()
        context1.set_mode("scientific")
        assert context1.get_mode() == "scientific"
        assert context2.get_mode() == "normal"


class TestGetMode:
    """Test CalculatorContext.get_mode() method."""

    def test_get_mode_returns_string(self):
        """Verify that get_mode() returns a string."""
        context = CalculatorContext()
        mode = context.get_mode()
        assert isinstance(mode, str)

    def test_get_mode_initial_returns_normal(self):
        """Verify that get_mode() initially returns 'normal'."""
        context = CalculatorContext()
        assert context.get_mode() == "normal"

    def test_get_mode_after_set_normal(self):
        """Verify that get_mode() returns 'normal' after setting to normal."""
        context = CalculatorContext()
        context.set_mode("normal")
        assert context.get_mode() == "normal"

    def test_get_mode_after_set_scientific(self):
        """Verify that get_mode() returns 'scientific' after setting to scientific."""
        context = CalculatorContext()
        context.set_mode("scientific")
        assert context.get_mode() == "scientific"

    def test_get_mode_matches_current_mode_attribute(self):
        """Verify that get_mode() matches current_mode attribute."""
        context = CalculatorContext()
        context.set_mode("scientific")
        assert context.get_mode() == context.current_mode


class TestSetMode:
    """Test CalculatorContext.set_mode() method."""

    def test_set_mode_normal(self):
        """Verify that set_mode('normal') works."""
        context = CalculatorContext()
        context.set_mode("normal")
        assert context.current_mode == "normal"

    def test_set_mode_scientific(self):
        """Verify that set_mode('scientific') works."""
        context = CalculatorContext()
        context.set_mode("scientific")
        assert context.current_mode == "scientific"

    def test_set_mode_to_scientific_from_normal(self):
        """Verify switching from normal to scientific."""
        context = CalculatorContext()
        assert context.get_mode() == "normal"
        context.set_mode("scientific")
        assert context.get_mode() == "scientific"

    def test_set_mode_to_normal_from_scientific(self):
        """Verify switching from scientific back to normal."""
        context = CalculatorContext()
        context.set_mode("scientific")
        context.set_mode("normal")
        assert context.get_mode() == "normal"

    def test_set_mode_multiple_times(self):
        """Verify setting mode multiple times in succession."""
        context = CalculatorContext()
        context.set_mode("scientific")
        assert context.get_mode() == "scientific"
        context.set_mode("normal")
        assert context.get_mode() == "normal"
        context.set_mode("scientific")
        assert context.get_mode() == "scientific"

    def test_set_mode_idempotent_normal(self):
        """Verify that setting to normal multiple times is idempotent."""
        context = CalculatorContext()
        context.set_mode("normal")
        context.set_mode("normal")
        assert context.get_mode() == "normal"

    def test_set_mode_idempotent_scientific(self):
        """Verify that setting to scientific multiple times is idempotent."""
        context = CalculatorContext()
        context.set_mode("scientific")
        context.set_mode("scientific")
        assert context.get_mode() == "scientific"

    def test_set_mode_invalid_empty_string(self):
        """Verify that set_mode('') raises ValueError."""
        context = CalculatorContext()
        with pytest.raises(ValueError, match="Invalid mode"):
            context.set_mode("")

    def test_set_mode_invalid_uppercase_normal(self):
        """Verify that set_mode('NORMAL') raises ValueError."""
        context = CalculatorContext()
        with pytest.raises(ValueError, match="Invalid mode"):
            context.set_mode("NORMAL")

    def test_set_mode_invalid_uppercase_scientific(self):
        """Verify that set_mode('SCIENTIFIC') raises ValueError."""
        context = CalculatorContext()
        with pytest.raises(ValueError, match="Invalid mode"):
            context.set_mode("SCIENTIFIC")

    def test_set_mode_invalid_mixed_case(self):
        """Verify that set_mode('Normal') raises ValueError."""
        context = CalculatorContext()
        with pytest.raises(ValueError, match="Invalid mode"):
            context.set_mode("Normal")

    def test_set_mode_invalid_typo(self):
        """Verify that set_mode('norma') raises ValueError."""
        context = CalculatorContext()
        with pytest.raises(ValueError, match="Invalid mode"):
            context.set_mode("norma")

    def test_set_mode_invalid_typo_scientific(self):
        """Verify that set_mode('scientifc') raises ValueError."""
        context = CalculatorContext()
        with pytest.raises(ValueError, match="Invalid mode"):
            context.set_mode("scientifc")

    def test_set_mode_invalid_with_whitespace(self):
        """Verify that set_mode with leading/trailing whitespace raises ValueError."""
        context = CalculatorContext()
        with pytest.raises(ValueError, match="Invalid mode"):
            context.set_mode(" normal")

    def test_set_mode_invalid_with_trailing_whitespace(self):
        """Verify that set_mode with trailing whitespace raises ValueError."""
        context = CalculatorContext()
        with pytest.raises(ValueError, match="Invalid mode"):
            context.set_mode("normal ")

    def test_set_mode_invalid_arbitrary_string(self):
        """Verify that set_mode('random_mode') raises ValueError."""
        context = CalculatorContext()
        with pytest.raises(ValueError, match="Invalid mode"):
            context.set_mode("random_mode")

    def test_set_mode_invalid_numeric_string(self):
        """Verify that set_mode('1') raises ValueError."""
        context = CalculatorContext()
        with pytest.raises(ValueError, match="Invalid mode"):
            context.set_mode("1")

    def test_set_mode_invalid_none(self):
        """Verify that set_mode(None) raises appropriate error."""
        context = CalculatorContext()
        # None is not a string, so it should fail when checked against strings
        with pytest.raises((ValueError, TypeError, AttributeError)):
            context.set_mode(None)  # type: ignore

    def test_set_mode_error_message_contains_valid_modes(self):
        """Verify that error message lists valid modes."""
        context = CalculatorContext()
        with pytest.raises(ValueError) as exc_info:
            context.set_mode("invalid")
        error_msg = str(exc_info.value)
        assert "normal" in error_msg or "scientific" in error_msg


class TestIsScientificMode:
    """Test CalculatorContext.is_scientific_mode() method."""

    def test_is_scientific_mode_initial_false(self):
        """Verify that is_scientific_mode() returns False initially."""
        context = CalculatorContext()
        assert context.is_scientific_mode() is False

    def test_is_scientific_mode_returns_bool(self):
        """Verify that is_scientific_mode() returns a boolean."""
        context = CalculatorContext()
        result = context.is_scientific_mode()
        assert isinstance(result, bool)

    def test_is_scientific_mode_true_in_scientific(self):
        """Verify that is_scientific_mode() returns True in scientific mode."""
        context = CalculatorContext()
        context.set_mode("scientific")
        assert context.is_scientific_mode() is True

    def test_is_scientific_mode_false_in_normal(self):
        """Verify that is_scientific_mode() returns False in normal mode."""
        context = CalculatorContext()
        context.set_mode("normal")
        assert context.is_scientific_mode() is False

    def test_is_scientific_mode_after_mode_switch(self):
        """Verify is_scientific_mode() after switching modes."""
        context = CalculatorContext()
        assert context.is_scientific_mode() is False
        context.set_mode("scientific")
        assert context.is_scientific_mode() is True
        context.set_mode("normal")
        assert context.is_scientific_mode() is False

    def test_is_scientific_mode_matches_get_mode(self):
        """Verify that is_scientific_mode() is consistent with get_mode()."""
        context = CalculatorContext()
        context.set_mode("scientific")
        assert context.is_scientific_mode() == (context.get_mode() == "scientific")
        context.set_mode("normal")
        assert context.is_scientific_mode() == (context.get_mode() == "scientific")

    def test_is_scientific_mode_multiple_calls_consistent(self):
        """Verify that multiple calls to is_scientific_mode() are consistent."""
        context = CalculatorContext()
        context.set_mode("scientific")
        result1 = context.is_scientific_mode()
        result2 = context.is_scientific_mode()
        assert result1 == result2 is True


class TestModeIntegration:
    """Integration tests for mode handling."""

    def test_set_mode_get_mode_is_scientific_consistency(self):
        """Verify consistency between set_mode, get_mode, and is_scientific_mode."""
        context = CalculatorContext()
        # Test normal mode
        context.set_mode("normal")
        assert context.get_mode() == "normal"
        assert context.is_scientific_mode() is False
        # Test scientific mode
        context.set_mode("scientific")
        assert context.get_mode() == "scientific"
        assert context.is_scientific_mode() is True

    def test_mode_state_persists_across_operations(self):
        """Verify that mode state persists across multiple operations."""
        context = CalculatorContext()
        context.set_mode("scientific")
        # Do some checks
        assert context.is_scientific_mode() is True
        assert context.get_mode() == "scientific"
        # Mode should still be scientific
        assert context.is_scientific_mode() is True

    def test_invalid_mode_does_not_change_state(self):
        """Verify that invalid set_mode() call doesn't change the state."""
        context = CalculatorContext()
        context.set_mode("scientific")
        original_mode = context.get_mode()
        try:
            context.set_mode("invalid")
        except ValueError:
            pass
        assert context.get_mode() == original_mode

    def test_mode_switch_sequence(self):
        """Verify a sequence of mode switches works correctly."""
        context = CalculatorContext()
        modes_to_test = ["normal", "scientific", "normal", "scientific", "normal"]
        expected = [False, True, False, True, False]
        for mode, expected_scientific in zip(modes_to_test, expected):
            context.set_mode(mode)
            assert context.is_scientific_mode() == expected_scientific
