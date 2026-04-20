"""Tests for mode switching in REPLInterface.

Tests cover:
- Mode initialization
- Mode command parsing ("mode normal", "mode scientific")
- Mode switching via get_operation_selection
- Menu display of current mode
- Trigonometric operations availability after mode switch
- Invalid mode commands
- Context integration
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.interface.repl import REPLInterface, MAX_RETRIES
from src.calculator import Calculator
from src.context import CalculatorContext
from src.support.exceptions import MaxRetriesExceeded


@pytest.fixture
def calc():
    """Provide a Calculator instance."""
    return Calculator()


@pytest.fixture
def context():
    """Provide a fresh CalculatorContext."""
    return CalculatorContext()


@pytest.fixture
def repl(calc, context):
    """Provide a REPLInterface instance with a context."""
    return REPLInterface(calc, error_logger=None, context=context)


@pytest.fixture
def repl_without_context(calc):
    """Provide a REPLInterface instance without explicit context."""
    return REPLInterface(calc, error_logger=None)


class TestREPLModeInitialization:
    """Test mode initialization in REPLInterface."""

    def test_repl_with_context_starts_in_normal(self, calc):
        """Verify REPL with context starts in normal mode."""
        context = CalculatorContext()
        repl = REPLInterface(calc, error_logger=None, context=context)
        assert repl._context.get_mode() == "normal"

    def test_repl_without_context_creates_fresh_context(self, repl_without_context):
        """Verify REPL creates fresh context when none provided."""
        assert repl_without_context._context is not None
        assert repl_without_context._context.get_mode() == "normal"

    def test_repl_context_synced_to_registry(self, calc, context):
        """Verify REPL syncs context mode to registry on initialization."""
        context.set_mode("scientific")
        repl = REPLInterface(calc, error_logger=None, context=context)
        assert repl._registry._current_mode == "scientific"

    def test_repl_operations_filtered_by_initial_mode(self, calc):
        """Verify REPL operations are filtered by initial mode."""
        context = CalculatorContext()
        repl = REPLInterface(calc, error_logger=None, context=context)
        # In normal mode, trig operations should not be in _operations
        operation_names = {op.name for op in repl._operations}
        assert "sin" not in operation_names
        assert "cos" not in operation_names
        assert "tan" not in operation_names

    def test_repl_operation_keys_match_operations(self, repl):
        """Verify REPL operation keys match operations list."""
        assert len(repl._operation_keys) == len(repl._operations)
        for i, op in enumerate(repl._operations):
            assert repl._operation_keys[i] == op.name


class TestREPLModeCommand:
    """Test mode command handling in get_operation_selection."""

    def test_mode_command_normal_from_normal(self, repl):
        """Verify 'mode normal' command in normal mode."""
        with patch("builtins.input", side_effect=["mode normal", "quit"]):
            result = repl.get_operation_selection()
        assert result == "quit"
        assert repl._context.get_mode() == "normal"

    def test_mode_command_scientific_from_normal(self, repl):
        """Verify switching to scientific mode with 'mode scientific'."""
        with patch("builtins.input", side_effect=["mode scientific", "quit"]):
            result = repl.get_operation_selection()
        assert result == "quit"
        assert repl._context.get_mode() == "scientific"

    def test_mode_command_normal_from_scientific(self, repl):
        """Verify switching back to normal mode."""
        repl._context.set_mode("scientific")
        repl._registry.set_mode("scientific")
        repl._refresh_operations()
        with patch("builtins.input", side_effect=["mode normal", "quit"]):
            result = repl.get_operation_selection()
        assert result == "quit"
        assert repl._context.get_mode() == "normal"

    def test_mode_command_case_insensitive(self, repl):
        """Verify mode command is case insensitive."""
        with patch("builtins.input", side_effect=["MODE SCIENTIFIC", "quit"]):
            result = repl.get_operation_selection()
        assert result == "quit"
        assert repl._context.get_mode() == "scientific"

    def test_mode_command_with_mixed_case(self, repl):
        """Verify mixed case mode command works."""
        with patch("builtins.input", side_effect=["Mode Scientific", "quit"]):
            result = repl.get_operation_selection()
        assert result == "quit"
        assert repl._context.get_mode() == "scientific"

    def test_mode_command_invalid_mode_rejected(self, repl):
        """Verify invalid mode name is rejected."""
        with patch("builtins.input", side_effect=["mode invalid", "quit"]):
            with patch("builtins.print"):
                result = repl.get_operation_selection()
        assert result == "quit"
        # Mode should not change
        assert repl._context.get_mode() == "normal"

    def test_mode_command_invalid_does_not_count_as_retry(self, repl):
        """Verify invalid mode command doesn't trigger retry limit."""
        # This should not raise MaxRetriesExceeded
        with patch("builtins.input", side_effect=[
            "mode invalid",
            "mode invalid",
            "mode invalid",
            "mode invalid",
            "quit"
        ]):
            with patch("builtins.print"):
                result = repl.get_operation_selection()
        assert result == "quit"

    def test_mode_command_refreshes_operations_list(self, repl):
        """Verify mode switch refreshes the operations list."""
        assert "sin" not in repl._operation_keys
        with patch("builtins.input", side_effect=["mode scientific", "quit"]):
            with patch("builtins.print"):
                result = repl.get_operation_selection()
        assert "sin" in repl._operation_keys
        assert "cos" in repl._operation_keys
        assert "tan" in repl._operation_keys

    def test_mode_command_updates_registry(self, repl):
        """Verify mode switch updates the registry."""
        assert repl._registry._current_mode == "normal"
        with patch("builtins.input", side_effect=["mode scientific", "quit"]):
            with patch("builtins.print"):
                result = repl.get_operation_selection()
        assert repl._registry._current_mode == "scientific"


class TestREPLModeMenuDisplay:
    """Test that mode is displayed in the menu."""

    def test_menu_displays_current_mode(self, repl):
        """Verify menu displays 'Current mode: normal'."""
        with patch("builtins.input", return_value="quit"):
            with patch("builtins.print") as mock_print:
                repl.get_operation_selection()
        # Check that "Current mode:" was printed
        printed_messages = [call[0][0] for call in mock_print.call_args_list]
        mode_displayed = any("Current mode:" in str(msg) for msg in printed_messages)
        assert mode_displayed

    def test_menu_displays_correct_mode_text(self, repl):
        """Verify menu displays the actual current mode."""
        repl._context.set_mode("scientific")
        with patch("builtins.input", return_value="quit"):
            with patch("builtins.print") as mock_print:
                repl.get_operation_selection()
        # Check that current mode is printed
        printed_messages = " ".join([str(call[0][0]) for call in mock_print.call_args_list])
        assert "scientific" in printed_messages

    def test_menu_shows_mode_instructions(self, repl):
        """Verify menu shows how to switch modes."""
        with patch("builtins.input", return_value="quit"):
            with patch("builtins.print") as mock_print:
                repl.get_operation_selection()
        # Check for mode instruction
        printed_messages = " ".join([str(call[0][0]) for call in mock_print.call_args_list])
        assert "mode" in printed_messages


class TestREPLTrigonometricAvailability:
    """Test trigonometric operation availability based on mode."""

    def test_trig_operations_not_in_normal_menu(self, repl):
        """Verify sin, cos, tan not in normal mode menu."""
        repl._context.set_mode("normal")
        repl._registry.set_mode("normal")
        repl._refresh_operations()
        operation_names = {op.name for op in repl._operations}
        assert "sin" not in operation_names
        assert "cos" not in operation_names
        assert "tan" not in operation_names

    def test_trig_operations_in_scientific_menu(self, repl):
        """Verify sin, cos, tan in scientific mode menu."""
        repl._context.set_mode("scientific")
        repl._registry.set_mode("scientific")
        repl._refresh_operations()
        operation_names = {op.name for op in repl._operations}
        assert "sin" in operation_names
        assert "cos" in operation_names
        assert "tan" in operation_names

    def test_can_select_sin_in_scientific_mode(self, repl):
        """Verify user can select sin operation in scientific mode."""
        repl._context.set_mode("scientific")
        repl._registry.set_mode("scientific")
        repl._refresh_operations()
        # Find the menu number for sin
        sin_index = next((i + 1 for i, op in enumerate(repl._operations) if op.name == "sin"), None)
        assert sin_index is not None
        with patch("builtins.input", return_value=str(sin_index)):
            result = repl.get_operation_selection()
        assert result == "sin"

    def test_cannot_select_sin_in_normal_mode(self, repl):
        """Verify user cannot select sin in normal mode (not in menu)."""
        repl._context.set_mode("normal")
        repl._registry.set_mode("normal")
        repl._refresh_operations()
        # Try to reference a sin operation (it won't exist in menu)
        max_menu_index = len(repl._operations)
        invalid_index = max_menu_index + 1
        with patch("builtins.input", side_effect=[str(invalid_index), "quit"]):
            with patch("builtins.print"):
                result = repl.get_operation_selection()
        assert result == "quit"


class TestREPLModeIntegration:
    """Integration tests for mode in REPL."""

    def test_mode_persists_through_operations(self, calc):
        """Verify mode persists across multiple operations."""
        context = CalculatorContext()
        repl = REPLInterface(calc, error_logger=None, context=context)
        # Switch to scientific
        with patch("builtins.input", side_effect=["mode scientific", "1"]):
            with patch("builtins.print"):
                repl.get_operation_selection()
        assert repl._context.get_mode() == "scientific"
        # Context should still be scientific
        assert context.get_mode() == "scientific"

    def test_shared_context_mode_between_repl_and_context(self, calc):
        """Verify REPL and context share mode state."""
        context = CalculatorContext()
        repl = REPLInterface(calc, error_logger=None, context=context)
        # Change via context
        context.set_mode("scientific")
        # REPL's registry should be updated when get_operation_selection is called
        # But first we need to manually sync (in real code this happens via mode command)
        repl._registry.set_mode(context.get_mode())
        repl._refresh_operations()
        assert "sin" in repl._operation_keys

    def test_separate_repl_instances_have_separate_contexts(self, calc):
        """Verify separate REPL instances have separate contexts."""
        repl1 = REPLInterface(calc, error_logger=None)
        repl2 = REPLInterface(calc, error_logger=None)
        # Change mode in repl1
        repl1._context.set_mode("scientific")
        # repl2 should still be in normal
        assert repl1._context.get_mode() == "scientific"
        assert repl2._context.get_mode() == "normal"

    def test_mode_command_sequence(self, repl):
        """Verify sequence of mode switches work correctly."""
        with patch("builtins.input", side_effect=[
            "mode scientific",
            "mode normal",
            "mode scientific",
            "quit"
        ]):
            with patch("builtins.print"):
                result = repl.get_operation_selection()
        assert result == "quit"
        assert repl._context.get_mode() == "scientific"

    def test_mode_affects_operation_execution(self, calc):
        """Verify mode affects which operations can be executed."""
        context = CalculatorContext()
        repl = REPLInterface(calc, error_logger=None, context=context)
        # In normal mode, sin should not be resolvable
        with pytest.raises(ValueError):
            repl._registry.resolve("sin")
        # Switch to scientific
        context.set_mode("scientific")
        repl._registry.set_mode("scientific")
        # Now sin should be resolvable
        assert repl._registry.resolve("sin") == "sin"
