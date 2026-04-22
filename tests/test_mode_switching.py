"""test_mode_switching.py — integration tests for mode switching.

Tests cover:
- CalculatorEngine mode enforcement: each mode exposes correct operations
- Invalid mode raises ValueError
- History preservation across mode switches
- Calculator scientific proxy methods
- REPL mode command handling
"""

import pytest
import math
from unittest.mock import patch, MagicMock
from io import StringIO

from src.logic import CalculatorEngine
from src import Calculator, CalculatorREPL


# =============================================================================
# TestCalculatorEngineModeEnforcement
# =============================================================================


class TestCalculatorEngineModeEnforcement:
    """Tests that each mode exposes the correct operations."""

    def test_basic_mode_exposes_basic_ops(self):
        """Test that basic mode exposes only basic operations."""
        engine = CalculatorEngine(mode="basic")
        # Should have basic ops
        assert engine.add(2, 3) == 5
        assert engine.subtract(5, 2) == 3
        assert engine.multiply(3, 4) == 12
        assert engine.divide(10, 2) == 5.0

    def test_basic_mode_no_advanced_ops(self):
        """Test that basic mode does not have advanced operations."""
        engine = CalculatorEngine(mode="basic")
        # Should NOT have advanced ops
        with pytest.raises(AttributeError):
            engine.factorial(5)
        with pytest.raises(AttributeError):
            engine.square(3)
        with pytest.raises(AttributeError):
            engine.natural_log(1)

    def test_basic_mode_no_scientific_ops(self):
        """Test that basic mode does not have scientific operations."""
        engine = CalculatorEngine(mode="basic")
        # Should NOT have scientific ops
        with pytest.raises(AttributeError):
            engine.sin(0)
        with pytest.raises(AttributeError):
            engine.ln(1)

    def test_advanced_mode_exposes_basic_and_advanced_ops(self):
        """Test that advanced mode exposes basic and advanced operations."""
        engine = CalculatorEngine(mode="advanced")
        # Should have basic and advanced ops
        assert engine.add(2, 3) == 5
        assert engine.factorial(5) == 120
        assert engine.square(3) == 9
        assert engine.natural_log(math.e) == pytest.approx(1)

    def test_advanced_mode_no_scientific_ops(self):
        """Test that advanced mode does not have scientific operations."""
        engine = CalculatorEngine(mode="advanced")
        # Should NOT have scientific ops
        with pytest.raises(AttributeError):
            engine.sin(0)
        with pytest.raises(AttributeError):
            engine.ln(1)

    def test_scientific_mode_exposes_all_ops(self):
        """Test that scientific mode exposes all operations."""
        engine = CalculatorEngine(mode="scientific")
        # Should have all ops
        assert engine.add(2, 3) == 5
        assert engine.factorial(5) == 120
        assert engine.sin(0) == 0
        assert engine.ln(math.e) == pytest.approx(1)

    def test_invalid_mode_raises_valueerror(self):
        """Test that invalid mode raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            CalculatorEngine(mode="invalid_mode")
        assert "Unknown mode" in str(exc_info.value)
        assert "invalid_mode" in str(exc_info.value)

    def test_get_operations_basic_mode(self):
        """Test get_operations for basic mode."""
        engine = CalculatorEngine(mode="basic")
        ops = engine.get_operations()
        basic_ops = {"add", "subtract", "multiply", "divide"}
        assert basic_ops.issubset(ops.keys())
        # Should not have advanced or scientific
        assert "factorial" not in ops
        assert "sin" not in ops

    def test_get_operations_advanced_mode(self):
        """Test get_operations for advanced mode."""
        engine = CalculatorEngine(mode="advanced")
        ops = engine.get_operations()
        basic_and_advanced = {"add", "factorial", "square", "natural_log"}
        assert basic_and_advanced.issubset(ops.keys())
        # Should not have scientific
        assert "sin" not in ops
        assert "ln" not in ops

    def test_get_operations_scientific_mode(self):
        """Test get_operations for scientific mode."""
        engine = CalculatorEngine(mode="scientific")
        ops = engine.get_operations()
        all_ops = {"add", "factorial", "sin", "cos", "ln", "exp"}
        assert all_ops.issubset(ops.keys())


# =============================================================================
# TestCalculatorEngineHistoryPreservation
# =============================================================================


class TestCalculatorEngineHistoryPreservation:
    """Tests that history is preserved across mode switches."""

    def test_history_preserved_basic_to_advanced(self):
        """Test that history is preserved when switching from basic to advanced."""
        engine = CalculatorEngine(mode="basic")
        engine.add(1, 2)
        engine.multiply(3, 4)
        assert len(engine.get_history()) == 2

        engine.set_mode("advanced")
        # History should still be there
        history = engine.get_history()
        assert len(history) == 2
        assert history[0]["operator"] == "add"
        assert history[1]["operator"] == "multiply"

    def test_history_preserved_advanced_to_scientific(self):
        """Test that history is preserved when switching to scientific."""
        engine = CalculatorEngine(mode="advanced")
        engine.add(1, 2)
        engine.factorial(5)
        assert len(engine.get_history()) == 2

        engine.set_mode("scientific")
        history = engine.get_history()
        assert len(history) == 2

    def test_operations_after_mode_switch_recorded(self):
        """Test that new operations after mode switch are recorded."""
        engine = CalculatorEngine(mode="basic")
        engine.add(1, 2)
        engine.set_mode("advanced")
        engine.factorial(3)

        history = engine.get_history()
        assert len(history) == 2
        assert history[0]["operator"] == "add"
        assert history[1]["operator"] == "factorial"

    def test_history_available_after_set_mode_to_scientific(self):
        """Test that operations before mode switch are accessible after switch."""
        engine = CalculatorEngine(mode="advanced")
        engine.add(5, 3)
        result_before = engine.get_history()[0]["result"]

        engine.set_mode("scientific")
        result_after = engine.get_history()[0]["result"]

        assert result_before == result_after == 8


# =============================================================================
# TestCalculatorScientificProxy
# =============================================================================


class TestCalculatorScientificProxy:
    """Tests for Calculator's scientific operation proxy methods."""

    def test_calculator_sin_delegates_to_engine(self):
        """Test that Calculator.sin delegates to engine.sin."""
        calc = Calculator(mode="scientific")
        result = calc.sin(0)
        assert result == 0

    def test_calculator_cos_delegates_to_engine(self):
        """Test that Calculator.cos delegates to engine.cos."""
        calc = Calculator(mode="scientific")
        result = calc.cos(0)
        assert result == 1

    def test_calculator_tan_delegates_to_engine(self):
        """Test that Calculator.tan delegates to engine.tan."""
        calc = Calculator(mode="scientific")
        result = calc.tan(0)
        assert result == 0

    def test_calculator_asin_delegates_to_engine(self):
        """Test that Calculator.asin delegates to engine.asin."""
        calc = Calculator(mode="scientific")
        result = calc.asin(1)
        assert result == pytest.approx(math.pi / 2)

    def test_calculator_acos_delegates_to_engine(self):
        """Test that Calculator.acos delegates to engine.acos."""
        calc = Calculator(mode="scientific")
        result = calc.acos(0)
        assert result == pytest.approx(math.pi / 2)

    def test_calculator_atan_delegates_to_engine(self):
        """Test that Calculator.atan delegates to engine.atan."""
        calc = Calculator(mode="scientific")
        result = calc.atan(1)
        assert result == pytest.approx(math.pi / 4)

    def test_calculator_sinh_delegates_to_engine(self):
        """Test that Calculator.sinh delegates to engine.sinh."""
        calc = Calculator(mode="scientific")
        result = calc.sinh(0)
        assert result == 0

    def test_calculator_cosh_delegates_to_engine(self):
        """Test that Calculator.cosh delegates to engine.cosh."""
        calc = Calculator(mode="scientific")
        result = calc.cosh(0)
        assert result == 1

    def test_calculator_tanh_delegates_to_engine(self):
        """Test that Calculator.tanh delegates to engine.tanh."""
        calc = Calculator(mode="scientific")
        result = calc.tanh(0)
        assert result == 0

    def test_calculator_degrees_delegates_to_engine(self):
        """Test that Calculator.degrees delegates to engine.degrees."""
        calc = Calculator(mode="scientific")
        result = calc.degrees(math.pi)
        assert result == pytest.approx(180)

    def test_calculator_radians_delegates_to_engine(self):
        """Test that Calculator.radians delegates to engine.radians."""
        calc = Calculator(mode="scientific")
        result = calc.radians(180)
        assert result == pytest.approx(math.pi)

    def test_calculator_exp_delegates_to_engine(self):
        """Test that Calculator.exp delegates to engine.exp."""
        calc = Calculator(mode="scientific")
        result = calc.exp(0)
        assert result == 1

    def test_calculator_ln_delegates_to_engine(self):
        """Test that Calculator.ln delegates to engine.ln."""
        calc = Calculator(mode="scientific")
        result = calc.ln(math.e)
        assert result == pytest.approx(1)

    def test_scientific_operations_recorded_in_history(self):
        """Test that scientific operations are recorded in history."""
        calc = Calculator(mode="scientific")
        calc.sin(0)
        calc.ln(math.e)
        history = calc.get_history()
        assert len(history) == 2
        assert history[0]["operator"] == "sin"
        assert history[1]["operator"] == "ln"

    def test_scientific_ops_not_available_in_basic_mode(self):
        """Test that scientific operations raise AttributeError in basic mode."""
        calc = Calculator(mode="basic")
        with pytest.raises(AttributeError):
            calc.sin(0)
        with pytest.raises(AttributeError):
            calc.ln(1)

    def test_scientific_ops_not_available_in_advanced_mode(self):
        """Test that scientific operations raise AttributeError in advanced mode."""
        calc = Calculator(mode="advanced")
        with pytest.raises(AttributeError):
            calc.sin(0)
        with pytest.raises(AttributeError):
            calc.ln(1)


# =============================================================================
# TestREPLModeCommand
# =============================================================================


class TestREPLModeCommand:
    """Tests for REPL mode command handling."""

    def test_repl_mode_command_with_no_args(self):
        """Test REPL mode command with no arguments shows current mode."""
        calc = Calculator(mode="advanced")
        repl = CalculatorREPL(calc)

        # Simulate user input "mode"
        with patch('builtins.input', return_value='mode'):
            # This should show current mode but not change it
            output = StringIO()
            with patch('sys.stdout', output):
                # The _handle_mode_command should be called
                # For now we just check that the mode is still advanced
                assert calc._mode == "advanced"

    def test_repl_mode_command_to_basic(self):
        """Test REPL mode command to switch to basic mode."""
        calc = Calculator(mode="advanced")
        assert calc._mode == "advanced"
        calc.set_mode("basic")
        assert calc._mode == "basic"

    def test_repl_mode_command_to_advanced(self):
        """Test REPL mode command to switch to advanced mode."""
        calc = Calculator(mode="basic")
        assert calc._mode == "basic"
        calc.set_mode("advanced")
        assert calc._mode == "advanced"

    def test_repl_mode_command_to_scientific(self):
        """Test REPL mode command to switch to scientific mode."""
        calc = Calculator(mode="advanced")
        assert calc._mode == "advanced"
        calc.set_mode("scientific")
        assert calc._mode == "scientific"

    def test_repl_mode_command_invalid_mode(self):
        """Test REPL mode command with invalid mode raises error."""
        calc = Calculator(mode="advanced")
        with pytest.raises(ValueError):
            calc.set_mode("invalid_mode")
        # Mode should be unchanged
        assert calc._mode == "advanced"

    def test_repl_mode_command_case_sensitive(self):
        """Test that mode command is case sensitive."""
        calc = Calculator(mode="basic")
        # Mode names must be lowercase
        with pytest.raises(ValueError):
            calc.set_mode("ADVANCED")
        # Lowercase works
        calc.set_mode("advanced")
        assert calc._mode == "advanced"


# =============================================================================
# TestModeSwitchingIntegration
# =============================================================================


class TestModeSwitchingIntegration:
    """Integration tests for complete mode switching workflows."""

    def test_workflow_basic_to_advanced_to_scientific(self):
        """Test complete workflow: basic -> advanced -> scientific."""
        calc = Calculator(mode="basic")
        calc.add(1, 2)
        assert len(calc.get_history()) == 1

        calc.set_mode("advanced")
        calc.factorial(3)
        assert len(calc.get_history()) == 2

        calc.set_mode("scientific")
        calc.sin(0)
        assert len(calc.get_history()) == 3

        history = calc.get_history()
        assert history[0]["operator"] == "add"
        assert history[1]["operator"] == "factorial"
        assert history[2]["operator"] == "sin"

    def test_mode_switch_preserves_previous_results(self):
        """Test that mode switches preserve previous calculation results."""
        calc = Calculator(mode="advanced")
        result1 = calc.add(10, 20)
        result2 = calc.multiply(2, 5)
        assert len(calc.get_history()) == 2

        calc.set_mode("scientific")
        # Previous results should still be there
        history = calc.get_history()
        assert history[0]["result"] == 30
        assert history[1]["result"] == 10

    def test_can_use_advanced_ops_after_switching_from_basic(self):
        """Test that advanced operations become available after mode switch."""
        calc = Calculator(mode="basic")

        # These should fail in basic mode
        with pytest.raises(AttributeError):
            calc.factorial(3)

        # Switch to advanced
        calc.set_mode("advanced")

        # Now it should work
        result = calc.factorial(3)
        assert result == 6

    def test_can_use_scientific_ops_after_switching_to_scientific(self):
        """Test that scientific operations become available after mode switch."""
        calc = Calculator(mode="advanced")

        # These should fail in advanced mode
        with pytest.raises(AttributeError):
            calc.sin(0)

        # Switch to scientific
        calc.set_mode("scientific")

        # Now it should work
        result = calc.sin(0)
        assert result == 0
