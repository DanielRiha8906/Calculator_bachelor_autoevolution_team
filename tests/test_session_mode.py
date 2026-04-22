"""Tests for CalculatorSession mode awareness and filtering."""

import pytest
from src.session import CalculatorSession
from src.core.calculator import Calculator
from src.mode import NORMAL_MODE_OPERATIONS, SCIENTIFIC_MODE_OPERATIONS


class TestCalculatorSessionModeManagement:
    """Test suite for CalculatorSession.set_mode() and get_current_mode()."""

    @pytest.fixture
    def session(self):
        """Fixture providing a CalculatorSession instance."""
        calculator = Calculator()
        return CalculatorSession(calculator)

    def test_set_mode_normal_returns_true(self, session):
        """Test set_mode('normal') returns True."""
        result = session.set_mode("normal")
        assert result is True

    def test_set_mode_scientific_returns_true(self, session):
        """Test set_mode('scientific') returns True."""
        result = session.set_mode("scientific")
        assert result is True

    def test_set_mode_invalid_returns_false(self, session):
        """Test set_mode with invalid mode returns False."""
        result = session.set_mode("invalid")
        assert result is False

    def test_get_current_mode_normal(self, session):
        """Test get_current_mode returns 'normal' after set_mode('normal')."""
        session.set_mode("normal")
        assert session.get_current_mode() == "normal"

    def test_get_current_mode_scientific(self, session):
        """Test get_current_mode returns 'scientific' after set_mode('scientific')."""
        session.set_mode("scientific")
        assert session.get_current_mode() == "scientific"

    def test_get_current_mode_initially_none(self, session):
        """Test get_current_mode returns None initially."""
        assert session.get_current_mode() is None

    def test_set_mode_with_mixed_case(self, session):
        """Test set_mode is case-insensitive ('NORMAL' -> 'normal')."""
        result = session.set_mode("NORMAL")
        assert result is True
        assert session.get_current_mode() == "normal"

    def test_set_mode_invalid_does_not_change_current_mode(self, session):
        """Test setting invalid mode does not change current mode."""
        session.set_mode("normal")
        session.set_mode("invalid")
        assert session.get_current_mode() == "normal"


class TestCalculatorSessionOperationFiltering:
    """Test suite for CalculatorSession operation list filtering by mode."""

    @pytest.fixture
    def session(self):
        """Fixture providing a CalculatorSession instance."""
        calculator = Calculator()
        return CalculatorSession(calculator)

    def test_normal_mode_excludes_trig_operations(self, session):
        """Test normal mode operation list excludes trigonometric operations."""
        session.set_mode("normal")
        ops = session.get_operation_list()
        trig_ops = ["sin", "cos", "tan", "cot", "asin", "acos"]
        for op in trig_ops:
            assert op not in ops

    def test_normal_mode_includes_normal_operations(self, session):
        """Test normal mode operation list includes all normal operations."""
        session.set_mode("normal")
        ops = session.get_operation_list()
        for op in NORMAL_MODE_OPERATIONS:
            assert op in ops

    def test_scientific_mode_includes_trig_operations(self, session):
        """Test scientific mode operation list includes trigonometric operations."""
        session.set_mode("scientific")
        ops = session.get_operation_list()
        trig_ops = ["sin", "cos", "tan", "cot", "asin", "acos"]
        for op in trig_ops:
            assert op in ops

    def test_scientific_mode_includes_advanced_operations(self, session):
        """Test scientific mode includes advanced operations like power, cube."""
        session.set_mode("scientific")
        ops = session.get_operation_list()
        advanced_ops = ["power", "cube", "cube_root", "factorial", "logarithm", "natural_logarithm"]
        for op in advanced_ops:
            assert op in ops

    def test_unset_mode_includes_all_operations(self, session):
        """Test unset mode (None) includes all operations (backward compat)."""
        # Don't set a mode
        ops = session.get_operation_list()
        all_ops = NORMAL_MODE_OPERATIONS + [
            "power", "cube", "cube_root", "factorial",
            "logarithm", "natural_logarithm", "sin", "cos", "tan", "cot", "asin", "acos"
        ]
        for op in all_ops:
            assert op in ops

    def test_switch_from_normal_to_scientific(self, session):
        """Test switching from normal to scientific mode updates operation list."""
        session.set_mode("normal")
        normal_ops = session.get_operation_list()

        session.set_mode("scientific")
        scientific_ops = session.get_operation_list()

        # Scientific should have more operations
        assert len(scientific_ops) > len(normal_ops)
        # Trig should be in scientific but not normal
        assert "sin" not in normal_ops
        assert "sin" in scientific_ops

    def test_switch_from_scientific_to_normal(self, session):
        """Test switching from scientific to normal mode updates operation list."""
        session.set_mode("scientific")
        scientific_ops = session.get_operation_list()

        session.set_mode("normal")
        normal_ops = session.get_operation_list()

        # Scientific should have more operations
        assert len(scientific_ops) > len(normal_ops)
        # Trig should be in scientific but not normal
        assert "sin" not in normal_ops
        assert "sin" in scientific_ops

    def test_operation_list_refreshes_after_mode_change(self, session):
        """Test operation list is refreshed after mode change."""
        session.set_mode("normal")
        ops1 = session.get_operation_list()

        session.set_mode("scientific")
        ops2 = session.get_operation_list()

        # Lists should be different
        assert ops1 != ops2

    def test_operation_list_does_not_contain_private_methods(self, session):
        """Test operation list does not contain private methods."""
        ops = session.get_operation_list()
        for op in ops:
            assert not op.startswith("_")

    def test_normal_mode_operation_count(self, session):
        """Test normal mode returns exactly the expected number of operations."""
        session.set_mode("normal")
        ops = session.get_operation_list()
        # Should be exactly the 6 normal operations
        assert len(ops) == len(NORMAL_MODE_OPERATIONS)

    def test_scientific_mode_operation_count(self, session):
        """Test scientific mode returns all operations."""
        session.set_mode("scientific")
        ops = session.get_operation_list()
        # Should be all operations (normal + scientific)
        assert len(ops) == len(SCIENTIFIC_MODE_OPERATIONS)
