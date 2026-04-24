"""Tests for scientific mode features in the calculator.

This module comprehensively tests:
1. Scientific operation functions (trigonometric, hyperbolic, exponential, constants)
2. Calculator mode state management (enable, disable, toggle scientific mode)
3. Calculator mode interaction with history recording
4. Interactive mode behavior (prompt_for_operator with scientific ops)
5. Display functions for mode changes
"""

import pytest
import math
from unittest.mock import patch
from src.calculator import Calculator


@pytest.fixture
def calculator():
    """Fixture providing a Calculator instance for tests."""
    return Calculator()


# ==============================================================================
# Scientific Operation Functions Tests
# ==============================================================================

class TestSin:
    """Test suite for the sin method."""

    def test_sin_basic(self, calculator):
        """Test sin(0) returns 0.0."""
        result = calculator.sin(0)
        assert result == pytest.approx(0.0, abs=1e-9)

    def test_sin_quarter_pi(self, calculator):
        """Test sin(π/2) returns 1.0."""
        result = calculator.sin(math.pi / 2)
        assert result == pytest.approx(1.0, abs=1e-9)


class TestCos:
    """Test suite for the cos method."""

    def test_cos_basic(self, calculator):
        """Test cos(0) returns 1.0."""
        result = calculator.cos(0)
        assert result == pytest.approx(1.0, abs=1e-9)

    def test_cos_half_pi(self, calculator):
        """Test cos(π) returns -1.0."""
        result = calculator.cos(math.pi)
        assert result == pytest.approx(-1.0, abs=1e-9)


class TestTan:
    """Test suite for the tan method."""

    def test_tan_basic(self, calculator):
        """Test tan(0) returns 0.0."""
        result = calculator.tan(0)
        assert result == pytest.approx(0.0, abs=1e-9)


class TestAsin:
    """Test suite for the asin method."""

    def test_asin_valid(self, calculator):
        """Test asin(0.5) returns π/6 (approx 0.5236)."""
        result = calculator.asin(0.5)
        assert result == pytest.approx(math.pi / 6, abs=1e-4)

    def test_asin_domain_error(self, calculator):
        """Test asin(1.5) raises ValueError (outside domain [-1, 1])."""
        with pytest.raises(ValueError):
            calculator.asin(1.5)


class TestAcos:
    """Test suite for the acos method."""

    def test_acos_valid(self, calculator):
        """Test acos(0.5) returns π/3 (approx 1.0472)."""
        result = calculator.acos(0.5)
        assert result == pytest.approx(math.pi / 3, abs=1e-4)

    @pytest.mark.parametrize("invalid_value", [2.0, -1.5])
    def test_acos_domain_error(self, calculator, invalid_value):
        """Test acos with values outside domain [-1, 1] raises ValueError."""
        with pytest.raises(ValueError):
            calculator.acos(invalid_value)


class TestAtan:
    """Test suite for the atan method."""

    def test_atan_basic(self, calculator):
        """Test atan(1) returns π/4 (approx 0.7854)."""
        result = calculator.atan(1)
        assert result == pytest.approx(math.pi / 4, abs=1e-4)


class TestSinh:
    """Test suite for the sinh method."""

    def test_sinh_basic(self, calculator):
        """Test sinh(0) returns 0.0."""
        result = calculator.sinh(0)
        assert result == pytest.approx(0.0, abs=1e-9)

    def test_sinh_positive(self, calculator):
        """Test sinh(1) returns approx 1.1752."""
        result = calculator.sinh(1)
        assert result == pytest.approx(1.1752, abs=1e-4)


class TestCosh:
    """Test suite for the cosh method."""

    def test_cosh_basic(self, calculator):
        """Test cosh(0) returns 1.0."""
        result = calculator.cosh(0)
        assert result == pytest.approx(1.0, abs=1e-9)


class TestTanh:
    """Test suite for the tanh method."""

    def test_tanh_basic(self, calculator):
        """Test tanh(0) returns 0.0."""
        result = calculator.tanh(0)
        assert result == pytest.approx(0.0, abs=1e-9)


class TestExp:
    """Test suite for the exp method."""

    def test_exp_zero(self, calculator):
        """Test exp(0) returns 1.0."""
        result = calculator.exp(0)
        assert result == pytest.approx(1.0, abs=1e-9)

    def test_exp_one(self, calculator):
        """Test exp(1) returns e (approx 2.71828)."""
        result = calculator.exp(1)
        assert result == pytest.approx(math.e, abs=1e-4)


class TestGetPi:
    """Test suite for the get_pi method."""

    def test_get_pi_constant(self, calculator):
        """Test get_pi() returns π (approx 3.14159)."""
        result = calculator.get_pi()
        assert result == pytest.approx(math.pi, abs=1e-5)


class TestGetE:
    """Test suite for the get_e method."""

    def test_get_e_constant(self, calculator):
        """Test get_e() returns e (approx 2.71828)."""
        result = calculator.get_e()
        assert result == pytest.approx(math.e, abs=1e-5)


# ==============================================================================
# Calculator Mode State Management Tests
# ==============================================================================

class TestCalculatorModeState:
    """Test suite for calculator mode state management."""

    def test_calculator_default_mode_normal(self, calculator):
        """Test that a fresh Calculator instance starts in normal mode."""
        assert calculator.is_scientific_mode() is False

    def test_calculator_enable_scientific_mode(self, calculator):
        """Test enable_scientific_mode() sets is_scientific_mode() to True."""
        calculator.enable_scientific_mode()
        assert calculator.is_scientific_mode() is True

    def test_calculator_disable_scientific_mode(self, calculator):
        """Test disable_scientific_mode() sets is_scientific_mode() to False."""
        calculator.enable_scientific_mode()
        calculator.disable_scientific_mode()
        assert calculator.is_scientific_mode() is False

    def test_calculator_toggle_scientific_mode(self, calculator):
        """Test toggle_scientific_mode() alternates the mode."""
        # Start: False
        assert calculator.is_scientific_mode() is False
        # After 1st toggle: True
        calculator.toggle_scientific_mode()
        assert calculator.is_scientific_mode() is True
        # After 2nd toggle: False
        calculator.toggle_scientific_mode()
        assert calculator.is_scientific_mode() is False
        # After 3rd toggle: True
        calculator.toggle_scientific_mode()
        assert calculator.is_scientific_mode() is True


# ==============================================================================
# History Recording with Scientific Operations Tests
# ==============================================================================

class TestScientificOperationHistory:
    """Test suite for history recording with scientific operations."""

    def test_scientific_operation_records_history(self, calculator):
        """Test that calling sin(0) records history entry."""
        calculator.sin(0)
        history = calculator.get_history()
        assert len(history) == 1
        assert history[0]["operation"] == "sin"
        assert history[0]["operands"] == [0]
        assert history[0]["result"] == pytest.approx(0.0, abs=1e-9)

    def test_constant_pi_records_history(self, calculator):
        """Test that get_pi() records history entry."""
        calculator.get_pi()
        history = calculator.get_history()
        assert len(history) == 1
        assert history[0]["operation"] == "get_pi"
        assert history[0]["operands"] == []
        assert history[0]["result"] == pytest.approx(math.pi, abs=1e-5)

    def test_constant_e_records_history(self, calculator):
        """Test that get_e() records history entry."""
        calculator.get_e()
        history = calculator.get_history()
        assert len(history) == 1
        assert history[0]["operation"] == "get_e"
        assert history[0]["operands"] == []
        assert history[0]["result"] == pytest.approx(math.e, abs=1e-5)


# ==============================================================================
# Mode State Consistency Tests
# ==============================================================================

class TestModeStateConsistency:
    """Test suite for mode state consistency."""

    def test_calculator_default_mode_is_normal(self, calculator):
        """Test that a fresh Calculator instance has is_scientific_mode() == False."""
        assert calculator.is_scientific_mode() is False

    def test_toggle_mode_cycles(self, calculator):
        """Test toggle cycles correctly: True -> False -> True."""
        # Initial state: False
        assert calculator.is_scientific_mode() is False
        # Toggle 1: True
        calculator.toggle_scientific_mode()
        assert calculator.is_scientific_mode() is True
        # Toggle 2: False
        calculator.toggle_scientific_mode()
        assert calculator.is_scientific_mode() is False
        # Toggle 3: True
        calculator.toggle_scientific_mode()
        assert calculator.is_scientific_mode() is True

    def test_scientific_ops_callable_independent_of_mode(self, calculator):
        """Test that scientific methods work regardless of mode setting."""
        # Calculator in normal mode, call calc.sin(0)
        assert calculator.is_scientific_mode() is False
        result = calculator.sin(0)
        # Should return 0.0 (Calendar methods always work; mode is a UI concern)
        assert result == pytest.approx(0.0, abs=1e-9)


# ==============================================================================
# Interactive Mode Interface Tests (prompt_for_operator with mode parameter)
# ==============================================================================

class TestModeToggleSentinels:
    """Test suite for mode toggle sentinel values from prompt_for_operator."""

    @patch("builtins.input", return_value="mode")
    def test_mode_toggle_sentinel_from_mode_command(self, mock_input):
        """Test prompt_for_operator receives 'mode' input returns 'MODE_TOGGLE'."""
        from src.interface import prompt_for_operator
        result = prompt_for_operator(mode="scientific")
        assert result == "MODE_TOGGLE"

    @patch("builtins.input", return_value="sci")
    def test_mode_toggle_sentinel_from_sci_command(self, mock_input):
        """Test prompt_for_operator receives 'sci' input returns 'MODE_TOGGLE'."""
        from src.interface import prompt_for_operator
        result = prompt_for_operator(mode="scientific")
        assert result == "MODE_TOGGLE"


class TestScientificOpsPromptMode:
    """Test suite for scientific operations in prompt_for_operator."""

    @patch("builtins.input", return_value="sin")
    def test_scientific_ops_accepted_in_scientific_mode(self, mock_input):
        """Test sin is accepted when prompt_for_operator called with mode='scientific'."""
        from src.interface import prompt_for_operator
        result = prompt_for_operator(mode="scientific")
        assert result == "sin"

    @patch("builtins.input", side_effect=["sin", "sin", "sin", "sin"])
    def test_scientific_ops_rejected_in_normal_mode(self, mock_input):
        """Test sin is rejected when prompt_for_operator called with mode='normal'."""
        from src.interface import prompt_for_operator
        with pytest.raises(Exception):
            # Should eventually raise an error after max retries with invalid 'sin' input
            prompt_for_operator(mode="normal")


# ==============================================================================
# Display Mode Change Tests
# ==============================================================================

class TestDisplayModeChange:
    """Test suite for display_mode_change function."""

    def test_display_mode_change_scientific(self, capsys):
        """Test display_mode_change('scientific') prints message with 'scientific'."""
        from src.interface import display_mode_change
        display_mode_change("scientific")
        captured = capsys.readouterr()
        assert "scientific" in captured.out.lower()

    def test_display_mode_change_normal(self, capsys):
        """Test display_mode_change('normal') prints message with 'normal'."""
        from src.interface import display_mode_change
        display_mode_change("normal")
        captured = capsys.readouterr()
        assert "normal" in captured.out.lower()
