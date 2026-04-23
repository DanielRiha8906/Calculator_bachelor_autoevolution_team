"""Unit tests for ModeManager class and CalculatorMode enum."""

import pytest
from src.mode_manager import CalculatorMode, ModeManager


class TestCalculatorModeEnum:
    """Test suite for CalculatorMode enum."""

    def test_calculator_mode_normal_value(self):
        """Test that NORMAL mode has correct string value."""
        assert CalculatorMode.NORMAL.value == "normal"

    def test_calculator_mode_scientific_value(self):
        """Test that SCIENTIFIC mode has correct string value."""
        assert CalculatorMode.SCIENTIFIC.value == "scientific"

    def test_calculator_mode_enum_members(self):
        """Test that CalculatorMode has exactly two members."""
        members = list(CalculatorMode)
        assert len(members) == 2
        assert CalculatorMode.NORMAL in members
        assert CalculatorMode.SCIENTIFIC in members


class TestModeManagerInitialization:
    """Test suite for ModeManager initialization."""

    def test_mode_manager_initializes_in_normal_mode(self):
        """Test that ModeManager starts in NORMAL mode."""
        manager = ModeManager()
        assert manager.get_current_mode() is CalculatorMode.NORMAL

    def test_mode_manager_get_current_mode_returns_enum(self):
        """Test that get_current_mode returns a CalculatorMode enum member."""
        manager = ModeManager()
        mode = manager.get_current_mode()
        assert isinstance(mode, CalculatorMode)


class TestModeManagerSwitch:
    """Test suite for ModeManager.switch_mode() method."""

    def test_switch_mode_toggles_normal_to_scientific(self):
        """Test that switch_mode changes NORMAL to SCIENTIFIC."""
        manager = ModeManager()
        assert manager.get_current_mode() is CalculatorMode.NORMAL
        manager.switch_mode()
        assert manager.get_current_mode() is CalculatorMode.SCIENTIFIC

    def test_switch_mode_toggles_scientific_to_normal(self):
        """Test that switch_mode changes SCIENTIFIC back to NORMAL."""
        manager = ModeManager()
        manager.switch_mode()
        assert manager.get_current_mode() is CalculatorMode.SCIENTIFIC
        manager.switch_mode()
        assert manager.get_current_mode() is CalculatorMode.NORMAL

    def test_switch_mode_cycles_correctly(self):
        """Test that calling switch_mode multiple times cycles correctly."""
        manager = ModeManager()
        initial_mode = manager.get_current_mode()
        manager.switch_mode()
        manager.switch_mode()
        assert manager.get_current_mode() is initial_mode


class TestModeManagerSetMode:
    """Test suite for ModeManager.set_mode() method."""

    def test_set_mode_to_scientific(self):
        """Test that set_mode can set mode to SCIENTIFIC."""
        manager = ModeManager()
        manager.set_mode(CalculatorMode.SCIENTIFIC)
        assert manager.get_current_mode() is CalculatorMode.SCIENTIFIC

    def test_set_mode_to_normal(self):
        """Test that set_mode can set mode to NORMAL."""
        manager = ModeManager()
        manager.switch_mode()
        manager.set_mode(CalculatorMode.NORMAL)
        assert manager.get_current_mode() is CalculatorMode.NORMAL

    def test_set_mode_with_string_raises_type_error(self):
        """Test that set_mode raises TypeError when given a string."""
        manager = ModeManager()
        with pytest.raises(TypeError, match="'mode' must be a CalculatorMode instance"):
            manager.set_mode("scientific")

    def test_set_mode_with_integer_raises_type_error(self):
        """Test that set_mode raises TypeError when given an integer."""
        manager = ModeManager()
        with pytest.raises(TypeError, match="'mode' must be a CalculatorMode instance"):
            manager.set_mode(1)

    def test_set_mode_with_none_raises_type_error(self):
        """Test that set_mode raises TypeError when given None."""
        manager = ModeManager()
        with pytest.raises(TypeError, match="'mode' must be a CalculatorMode instance"):
            manager.set_mode(None)

    @pytest.mark.parametrize("invalid_input", [
        "normal", "NORMAL", "Normal",
        "SCIENTIFIC", 0, 1, True, False,
        [], {}, (1, 2), 3.14,
    ])
    def test_set_mode_with_various_invalid_types(self, invalid_input):
        """Test that set_mode raises TypeError for various non-CalculatorMode inputs."""
        manager = ModeManager()
        with pytest.raises(TypeError):
            manager.set_mode(invalid_input)


class TestModeManagerGetModeDisplayName:
    """Test suite for ModeManager.get_mode_display_name() method."""

    def test_get_mode_display_name_normal_mode(self):
        """Test that display name for NORMAL mode is 'Normal'."""
        manager = ModeManager()
        assert manager.get_mode_display_name() == "Normal"

    def test_get_mode_display_name_scientific_mode(self):
        """Test that display name for SCIENTIFIC mode is 'Scientific'."""
        manager = ModeManager()
        manager.switch_mode()
        assert manager.get_mode_display_name() == "Scientific"

    def test_get_mode_display_name_returns_string(self):
        """Test that get_mode_display_name returns a string."""
        manager = ModeManager()
        result = manager.get_mode_display_name()
        assert isinstance(result, str)

    def test_get_mode_display_name_after_set_mode(self):
        """Test that display name is correct after using set_mode."""
        manager = ModeManager()
        manager.set_mode(CalculatorMode.SCIENTIFIC)
        assert manager.get_mode_display_name() == "Scientific"
        manager.set_mode(CalculatorMode.NORMAL)
        assert manager.get_mode_display_name() == "Normal"


class TestModeManagerIsOperationAvailable:
    """Test suite for ModeManager.is_operation_available() method."""

    def test_is_operation_available_normal_mode_non_scientific_op(self):
        """Test that non-scientific operations are available in NORMAL mode."""
        manager = ModeManager()
        scientific_ops = {"sin", "cos", "tan"}
        assert manager.is_operation_available("add", scientific_ops) is True

    def test_is_operation_available_normal_mode_scientific_op(self):
        """Test that scientific operations are NOT available in NORMAL mode."""
        manager = ModeManager()
        scientific_ops = {"sin", "cos", "tan"}
        assert manager.is_operation_available("sin", scientific_ops) is False

    def test_is_operation_available_scientific_mode_non_scientific_op(self):
        """Test that non-scientific operations are available in SCIENTIFIC mode."""
        manager = ModeManager()
        manager.switch_mode()
        scientific_ops = {"sin", "cos", "tan"}
        assert manager.is_operation_available("add", scientific_ops) is True

    def test_is_operation_available_scientific_mode_scientific_op(self):
        """Test that scientific operations ARE available in SCIENTIFIC mode."""
        manager = ModeManager()
        manager.switch_mode()
        scientific_ops = {"sin", "cos", "tan"}
        assert manager.is_operation_available("sin", scientific_ops) is True

    @pytest.mark.parametrize("sci_op", ["sin", "cos", "tan"])
    def test_is_operation_available_scientific_ops_in_normal_mode(self, sci_op):
        """Test that each scientific op is unavailable in NORMAL mode."""
        manager = ModeManager()
        scientific_ops = {"sin", "cos", "tan"}
        assert manager.is_operation_available(sci_op, scientific_ops) is False

    @pytest.mark.parametrize("sci_op", ["sin", "cos", "tan"])
    def test_is_operation_available_scientific_ops_in_scientific_mode(self, sci_op):
        """Test that each scientific op is available in SCIENTIFIC mode."""
        manager = ModeManager()
        manager.switch_mode()
        scientific_ops = {"sin", "cos", "tan"}
        assert manager.is_operation_available(sci_op, scientific_ops) is True

    @pytest.mark.parametrize("normal_op", ["add", "subtract", "multiply", "divide"])
    def test_is_operation_available_normal_ops_in_both_modes(self, normal_op):
        """Test that normal operations are available in both modes."""
        scientific_ops = {"sin", "cos", "tan"}
        # Test in NORMAL mode
        manager_normal = ModeManager()
        assert manager_normal.is_operation_available(normal_op, scientific_ops) is True
        # Test in SCIENTIFIC mode
        manager_sci = ModeManager()
        manager_sci.switch_mode()
        assert manager_sci.is_operation_available(normal_op, scientific_ops) is True

    def test_is_operation_available_empty_scientific_set(self):
        """Test behavior when scientific_operations set is empty."""
        manager = ModeManager()
        scientific_ops = set()
        assert manager.is_operation_available("add", scientific_ops) is True
        assert manager.is_operation_available("sin", scientific_ops) is True

    def test_is_operation_available_returns_boolean(self):
        """Test that is_operation_available returns a boolean."""
        manager = ModeManager()
        result = manager.is_operation_available("add", {"sin"})
        assert isinstance(result, bool)
