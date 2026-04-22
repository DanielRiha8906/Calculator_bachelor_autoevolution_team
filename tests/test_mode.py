"""Tests for mode.py: CalculatorMode enum, operation lists, and ModeConfig."""

import pytest
from src.mode import (
    CalculatorMode,
    ModeConfig,
    NORMAL_MODE_OPERATIONS,
    SCIENTIFIC_MODE_OPERATIONS,
    get_mode_config,
)


class TestCalculatorModeEnum:
    """Test suite for CalculatorMode enum."""

    def test_normal_mode_value(self):
        """Test NORMAL mode has correct string value."""
        assert CalculatorMode.NORMAL.value == "normal"

    def test_scientific_mode_value(self):
        """Test SCIENTIFIC mode has correct string value."""
        assert CalculatorMode.SCIENTIFIC.value == "scientific"


class TestNormalModeOperations:
    """Test suite for NORMAL_MODE_OPERATIONS list."""

    def test_normal_mode_operations_contains_expected_ops(self):
        """Test NORMAL_MODE_OPERATIONS contains exactly 6 operations."""
        expected = ["add", "subtract", "multiply", "divide", "square", "square_root"]
        assert NORMAL_MODE_OPERATIONS == expected

    def test_normal_mode_operations_is_list(self):
        """Test NORMAL_MODE_OPERATIONS is a list."""
        assert isinstance(NORMAL_MODE_OPERATIONS, list)

    def test_normal_mode_operations_length(self):
        """Test NORMAL_MODE_OPERATIONS has length 6."""
        assert len(NORMAL_MODE_OPERATIONS) == 6

    def test_all_elements_are_strings(self):
        """Test all elements in NORMAL_MODE_OPERATIONS are strings."""
        assert all(isinstance(op, str) for op in NORMAL_MODE_OPERATIONS)


class TestScientificModeOperations:
    """Test suite for SCIENTIFIC_MODE_OPERATIONS list."""

    def test_scientific_mode_includes_normal_operations(self):
        """Test SCIENTIFIC_MODE_OPERATIONS includes all normal operations."""
        for op in NORMAL_MODE_OPERATIONS:
            assert op in SCIENTIFIC_MODE_OPERATIONS

    def test_scientific_mode_includes_trig_operations(self):
        """Test SCIENTIFIC_MODE_OPERATIONS includes trigonometric operations."""
        trig_ops = ["sin", "cos", "tan", "cot", "asin", "acos"]
        for op in trig_ops:
            assert op in SCIENTIFIC_MODE_OPERATIONS

    def test_scientific_mode_includes_advanced_operations(self):
        """Test SCIENTIFIC_MODE_OPERATIONS includes advanced operations."""
        advanced_ops = ["power", "cube", "cube_root", "factorial", "logarithm", "natural_logarithm"]
        for op in advanced_ops:
            assert op in SCIENTIFIC_MODE_OPERATIONS

    def test_scientific_mode_has_more_ops_than_normal(self):
        """Test SCIENTIFIC_MODE_OPERATIONS has more operations than NORMAL."""
        assert len(SCIENTIFIC_MODE_OPERATIONS) > len(NORMAL_MODE_OPERATIONS)

    def test_trig_not_in_normal_mode(self):
        """Test trigonometric operations are NOT in NORMAL_MODE_OPERATIONS."""
        trig_ops = ["sin", "cos", "tan", "cot", "asin", "acos"]
        for op in trig_ops:
            assert op not in NORMAL_MODE_OPERATIONS

    def test_scientific_is_list(self):
        """Test SCIENTIFIC_MODE_OPERATIONS is a list."""
        assert isinstance(SCIENTIFIC_MODE_OPERATIONS, list)

    def test_all_elements_are_strings(self):
        """Test all elements in SCIENTIFIC_MODE_OPERATIONS are strings."""
        assert all(isinstance(op, str) for op in SCIENTIFIC_MODE_OPERATIONS)


class TestModeConfigDataclass:
    """Test suite for ModeConfig dataclass."""

    def test_mode_config_creation(self):
        """Test ModeConfig can be instantiated."""
        config = ModeConfig(
            mode=CalculatorMode.NORMAL,
            operations=["add", "subtract"]
        )
        assert config.mode == CalculatorMode.NORMAL
        assert config.operations == ["add", "subtract"]

    def test_mode_config_has_mode_attribute(self):
        """Test ModeConfig has mode attribute."""
        config = ModeConfig(
            mode=CalculatorMode.SCIENTIFIC,
            operations=[]
        )
        assert hasattr(config, "mode")

    def test_mode_config_has_operations_attribute(self):
        """Test ModeConfig has operations attribute."""
        config = ModeConfig(
            mode=CalculatorMode.NORMAL,
            operations=["add"]
        )
        assert hasattr(config, "operations")


class TestGetModeConfig:
    """Test suite for get_mode_config() factory function."""

    def test_get_mode_config_normal(self):
        """Test get_mode_config returns ModeConfig for 'normal'."""
        config = get_mode_config("normal")
        assert config is not None
        assert config.mode == CalculatorMode.NORMAL
        assert config.operations == NORMAL_MODE_OPERATIONS

    def test_get_mode_config_scientific(self):
        """Test get_mode_config returns ModeConfig for 'scientific'."""
        config = get_mode_config("scientific")
        assert config is not None
        assert config.mode == CalculatorMode.SCIENTIFIC
        assert config.operations == SCIENTIFIC_MODE_OPERATIONS

    def test_get_mode_config_case_insensitive_normal(self):
        """Test get_mode_config is case-insensitive for 'NORMAL'."""
        config = get_mode_config("NORMAL")
        assert config is not None
        assert config.mode == CalculatorMode.NORMAL

    def test_get_mode_config_case_insensitive_scientific(self):
        """Test get_mode_config is case-insensitive for 'SCIENTIFIC'."""
        config = get_mode_config("SCIENTIFIC")
        assert config is not None
        assert config.mode == CalculatorMode.SCIENTIFIC

    def test_get_mode_config_mixed_case(self):
        """Test get_mode_config handles mixed case 'Normal'."""
        config = get_mode_config("Normal")
        assert config is not None
        assert config.mode == CalculatorMode.NORMAL

    def test_get_mode_config_invalid_mode(self):
        """Test get_mode_config returns None for invalid mode."""
        config = get_mode_config("invalid")
        assert config is None

    def test_get_mode_config_empty_string(self):
        """Test get_mode_config returns None for empty string."""
        config = get_mode_config("")
        assert config is None

    def test_get_mode_config_returns_modeconfig_type(self):
        """Test get_mode_config returns ModeConfig instance."""
        config = get_mode_config("normal")
        assert isinstance(config, ModeConfig)

    def test_get_mode_config_operations_are_lists(self):
        """Test returned ModeConfig operations are list instances."""
        normal_config = get_mode_config("normal")
        scientific_config = get_mode_config("scientific")
        assert isinstance(normal_config.operations, list)
        assert isinstance(scientific_config.operations, list)

    def test_get_mode_config_operations_are_copies(self):
        """Test returned operations lists are independent copies."""
        config1 = get_mode_config("normal")
        config2 = get_mode_config("normal")
        # Modify one list
        config1.operations.append("fake_operation")
        # Verify the other is not affected
        assert "fake_operation" not in config2.operations
