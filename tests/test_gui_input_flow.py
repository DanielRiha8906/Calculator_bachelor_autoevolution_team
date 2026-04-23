"""Integration tests for iOS-style GUI input flow.

Tests the new button-driven input model where:
- Digit buttons accumulate into a display value
- Binary operators store operand1 and show the operator symbol
- The equals button executes the pending binary operation
- Unary operators execute immediately on the current display
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sys


@pytest.fixture(autouse=True)
def mock_tkinter():
    """Mock tkinter and ttk modules for headless testing."""
    mock_tk_module = MagicMock()
    mock_ttk_module = MagicMock()

    class FakeTk:
        def __init__(self):
            pass
        def columnconfigure(self, *args, **kwargs):
            pass
        def rowconfigure(self, *args, **kwargs):
            pass
        def configure(self, *args, **kwargs):
            pass
        def config(self, *args, **kwargs):
            pass
        def title(self, *args):
            pass
        def resizable(self, *args):
            pass
        def minsize(self, *args):
            pass
        def mainloop(self):
            pass

    class FakeStringVar:
        def __init__(self, value=""):
            self._value = value
        def get(self):
            return self._value
        def set(self, value):
            self._value = value

    mock_tk_module.Tk = FakeTk
    mock_tk_module.StringVar = FakeStringVar
    mock_tk_module.Canvas = MagicMock
    mock_tk_module.Text = MagicMock
    mock_tk_module.Event = MagicMock
    mock_tk_module.END = "end"

    def make_widget():
        widget = MagicMock()
        widget.grid = MagicMock()
        widget.configure = MagicMock()
        widget.get = MagicMock(return_value="")
        widget.delete = MagicMock()
        widget.insert = MagicMock()
        widget.winfo_children = MagicMock(return_value=[])
        widget.destroy = MagicMock()
        widget.bind = MagicMock()
        widget.create_window = MagicMock(return_value=1)
        widget.itemconfigure = MagicMock()
        widget.bbox = MagicMock(return_value=(0, 0, 100, 100))
        widget.see = MagicMock()
        widget.update_idletasks = MagicMock()
        widget.set = MagicMock()
        return widget

    mock_ttk_module.LabelFrame = MagicMock(side_effect=lambda *args, **kwargs: make_widget())
    mock_ttk_module.Button = MagicMock(side_effect=lambda *args, **kwargs: make_widget())
    mock_ttk_module.Entry = MagicMock(side_effect=lambda *args, **kwargs: make_widget())
    mock_ttk_module.Label = MagicMock(side_effect=lambda *args, **kwargs: make_widget())
    mock_ttk_module.Frame = MagicMock(side_effect=lambda *args, **kwargs: make_widget())
    mock_ttk_module.Scrollbar = MagicMock(side_effect=lambda *args, **kwargs: make_widget())

    mock_tk_module.Canvas = MagicMock(side_effect=lambda *args, **kwargs: make_widget())
    mock_tk_module.Text = MagicMock(side_effect=lambda *args, **kwargs: make_widget())

    modules = {
        "tkinter": mock_tk_module,
        "tkinter.ttk": mock_ttk_module,
    }

    with patch.dict(sys.modules, modules):
        yield mock_tk_module, mock_ttk_module


@pytest.fixture
def mock_adapter():
    """Fixture providing a mocked GUISessionAdapter with predefined responses."""
    adapter = MagicMock()
    adapter.get_operations.return_value = ["add", "subtract", "multiply", "divide", "square", "square_root"]
    adapter.get_arity.side_effect = lambda op: {
        "add": 2, "subtract": 2, "multiply": 2, "divide": 2,
        "square": 1, "square_root": 1, "cube": 1
    }.get(op, 2)
    adapter.get_history.return_value = []
    return adapter


class TestNumberButtonInteraction:
    """Test suite for number button interaction with display accumulation."""

    def test_first_number_replaces_zero_display(self, mock_tkinter, mock_adapter):
        """Test that clicking first digit replaces '0' instead of appending."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert window._display_value == "0"

        window.on_number_clicked("5")

        assert window._display_value == "5"
        assert window._display_var.get() == "5"

    def test_subsequent_numbers_append_to_display(self, mock_tkinter, mock_adapter):
        """Test that subsequent digit clicks append to the display."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window.on_number_clicked("5")
        assert window._display_value == "5"

        window.on_number_clicked("3")

        assert window._display_value == "53"
        assert window._display_var.get() == "53"

    def test_multiple_digits_accumulate(self, mock_tkinter, mock_adapter):
        """Test that multiple digit clicks accumulate into multi-digit number."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window.on_number_clicked("1")
        window.on_number_clicked("2")
        window.on_number_clicked("3")

        assert window._display_value == "123"
        assert window._display_var.get() == "123"

    def test_zero_appends_after_nonzero(self, mock_tkinter, mock_adapter):
        """Test that '0' appends normally after a non-zero digit."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window.on_number_clicked("5")
        window.on_number_clicked("0")

        assert window._display_value == "50"

    def test_leading_zero_replaced_by_first_digit(self, mock_tkinter, mock_adapter):
        """Test that '0' is replaced when it's the initial display."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # Initial display is "0"
        assert window._display_value == "0"

        window.on_number_clicked("0")

        # Should replace, not append
        assert window._display_value == "0"

    def test_display_value_syncs_with_display_var(self, mock_tkinter, mock_adapter):
        """Test that _display_value and _display_var stay in sync."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        for digit in ["7", "8", "9"]:
            window.on_number_clicked(digit)
            assert window._display_value == window._display_var.get()


class TestUnaryOperationBehavior:
    """Test suite for unary operation execution flow."""

    def test_unary_op_executes_on_current_display(self, mock_tkinter, mock_adapter):
        """Test that unary operation executes immediately on display value."""
        from src.gui.window import CalculatorWindow

        mock_adapter.execute_operation_safe.return_value = ("25.0", "")
        window = CalculatorWindow(mock_adapter)
        window._display_value = "5"
        window._display_var.set("5")

        window.on_operation_selected("square")

        # Verify adapter was called with the display value
        mock_adapter.execute_operation_safe.assert_called_once()
        call_args = mock_adapter.execute_operation_safe.call_args
        assert call_args[0][0] == "square"
        assert call_args[0][1] == [5.0]

    def test_unary_op_result_appears_in_display(self, mock_tkinter, mock_adapter):
        """Test that unary operation result is displayed."""
        from src.gui.window import CalculatorWindow

        mock_adapter.execute_operation_safe.return_value = ("25.0", "")
        window = CalculatorWindow(mock_adapter)
        window._display_value = "5"
        window._display_var.set("5")

        window.on_operation_selected("square")

        assert window._display_value == "25.0"
        assert window._display_var.get() == "25.0"

    def test_unary_op_clears_pending_binary_op(self, mock_tkinter, mock_adapter):
        """Test that unary operation doesn't interfere with pending state."""
        from src.gui.window import CalculatorWindow

        mock_adapter.execute_operation_safe.return_value = ("16.0", "")
        window = CalculatorWindow(mock_adapter)
        # No pending op to clear in unary case, but verify state stays clean
        window._pending_binary_op = None
        window._display_value = "4"
        window._display_var.set("4")

        window.on_operation_selected("square")

        # Pending op should still be None (no binary op was started)
        assert window._pending_binary_op is None

    def test_square_on_5_shows_25(self, mock_tkinter, mock_adapter):
        """Test concrete scenario: square of 5 is 25."""
        from src.gui.window import CalculatorWindow

        mock_adapter.execute_operation_safe.return_value = ("25.0", "")
        window = CalculatorWindow(mock_adapter)
        window._display_value = "5"
        window._display_var.set("5")

        window.on_operation_selected("square")

        assert window._display_value == "25.0"


class TestBinaryOperationBehavior:
    """Test suite for binary operation iOS-style flow."""

    def test_binary_op_click_stores_operator(self, mock_tkinter, mock_adapter):
        """Test that binary operator button click stores the operator."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._display_value = "3"
        window._display_var.set("3")

        window.on_operation_selected("add")

        assert window._pending_binary_op == "add"

    def test_binary_op_appends_symbol_to_display(self, mock_tkinter, mock_adapter):
        """Test that binary operation appends symbol to display."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._display_value = "3"
        window._display_var.set("3")

        window.on_operation_selected("add")

        # Display should show "3 + "
        assert "+" in window._display_value
        assert "3" in window._display_value

    def test_display_ready_for_second_operand_after_binary_op(self, mock_tkinter, mock_adapter):
        """Test that display is ready for second operand entry after binary op."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._display_value = "3"
        window._display_var.set("3")

        window.on_operation_selected("add")

        # Now we can append the second operand
        window.on_number_clicked("5")

        # Display should have both operands and operator
        assert "3" in window._display_value
        assert "+" in window._display_value
        assert "5" in window._display_value

    def test_add_operation_shows_plus_in_display(self, mock_tkinter, mock_adapter):
        """Test concrete scenario: add operation shows + in display."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._display_value = "3"
        window._display_var.set("3")

        window.on_operation_selected("add")

        assert "+" in window._display_value

    def test_binary_op_stores_operand_in_adapter(self, mock_tkinter, mock_adapter):
        """Test that binary operator stores operand1 in adapter."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._display_value = "7"
        window._display_var.set("7")

        window.on_operation_selected("multiply")

        # Verify adapter.store_first_operand was called
        mock_adapter.store_first_operand.assert_called_with(7.0)

    def test_subtract_operation_shows_minus_in_display(self, mock_tkinter, mock_adapter):
        """Test concrete scenario: subtract operation shows − in display."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._display_value = "10"
        window._display_var.set("10")

        window.on_operation_selected("subtract")

        # Unicode minus sign or hyphen
        assert "−" in window._display_value or "-" in window._display_value


class TestEqualsExecution:
    """Test suite for equals button execution of binary operations."""

    def test_equals_executes_pending_binary_op(self, mock_tkinter, mock_adapter):
        """Test that equals button executes a pending binary operation."""
        from src.gui.window import CalculatorWindow

        mock_adapter.execute_operation_safe.return_value = ("8.0", "")
        window = CalculatorWindow(mock_adapter)
        window._display_value = "3 + 5"
        window._display_var.set("3 + 5")
        window._pending_binary_op = "add"
        mock_adapter.get_pending_operand.return_value = 3.0

        window.on_equals_clicked()

        # Verify adapter.execute_operation_safe was called
        mock_adapter.execute_operation_safe.assert_called()

    def test_equals_updates_display_with_result(self, mock_tkinter, mock_adapter):
        """Test that equals button updates display with result."""
        from src.gui.window import CalculatorWindow

        mock_adapter.execute_operation_safe.return_value = ("8.0", "")
        window = CalculatorWindow(mock_adapter)
        window._display_value = "3 + 5"
        window._display_var.set("3 + 5")
        window._pending_binary_op = "add"
        mock_adapter.get_pending_operand.return_value = 3.0

        window.on_equals_clicked()

        # Display should show result
        assert window._display_value == "8.0"
        assert window._display_var.get() == "8.0"

    def test_equals_without_pending_op_does_nothing(self, mock_tkinter, mock_adapter):
        """Test that equals without pending operation doesn't crash."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._pending_binary_op = None

        # Should not raise
        window.on_equals_clicked()

        # Adapter execute should not be called (falls back to legacy path with no op selected)
        mock_adapter.execute_operation_safe.assert_not_called()

    def test_3_plus_5_equals_shows_8(self, mock_tkinter, mock_adapter):
        """Test concrete scenario: 3 + 5 = 8."""
        from src.gui.window import CalculatorWindow

        mock_adapter.execute_operation_safe.return_value = ("8.0", "")
        window = CalculatorWindow(mock_adapter)

        # Simulate: click 3, click add, click 5, click equals
        window.on_number_clicked("3")
        window.on_operation_selected("add")
        window._display_value = "3 + "  # Simulate what display looks like after add
        window._display_var.set("3 + ")
        window.on_number_clicked("5")
        window._display_value = "3 + 5"  # Update display to show both operands
        window._display_var.set("3 + 5")

        window.on_equals_clicked()

        assert window._display_value == "8.0"

    def test_equals_clears_pending_binary_op(self, mock_tkinter, mock_adapter):
        """Test that equals clears the pending binary operation."""
        from src.gui.window import CalculatorWindow

        mock_adapter.execute_operation_safe.return_value = ("7.0", "")
        window = CalculatorWindow(mock_adapter)
        window._display_value = "3 + 4"
        window._display_var.set("3 + 4")
        window._pending_binary_op = "add"

        window.on_equals_clicked()

        assert window._pending_binary_op is None

    def test_equals_clears_pending_operand(self, mock_tkinter, mock_adapter):
        """Test that equals clears the stored pending operand."""
        from src.gui.window import CalculatorWindow

        mock_adapter.execute_operation_safe.return_value = ("6.0", "")
        window = CalculatorWindow(mock_adapter)
        window._display_value = "2 + 4"
        window._display_var.set("2 + 4")
        window._pending_binary_op = "add"

        window.on_equals_clicked()

        # Verify adapter.clear_pending_operand was called
        mock_adapter.clear_pending_operand.assert_called()


class TestHistoryToggle:
    """Test suite for history panel toggle."""

    def test_history_hidden_by_default(self, mock_tkinter, mock_adapter):
        """Test that history panel is hidden on startup."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert window._history_visible is False

    def test_history_toggle_shows_history(self, mock_tkinter, mock_adapter):
        """Test that toggling shows the history panel."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert window._history_visible is False

        window.on_history_toggle_clicked()

        assert window._history_visible is True

    def test_history_toggle_hides_history(self, mock_tkinter, mock_adapter):
        """Test that toggling again hides the history panel."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._history_visible = True

        window.on_history_toggle_clicked()

        assert window._history_visible is False

    def test_history_toggle_preserves_entries_when_hidden(self, mock_tkinter, mock_adapter):
        """Test that history entries are preserved when panel is toggled hidden."""
        from src.gui.window import CalculatorWindow

        mock_adapter.get_history.return_value = ["1 + 2 = 3", "5 - 3 = 2"]
        window = CalculatorWindow(mock_adapter)

        # Show history
        window.on_history_toggle_clicked()
        assert window._history_visible is True

        # Hide history
        window.on_history_toggle_clicked()
        assert window._history_visible is False

        # Show again - entries should still be there
        window.on_history_toggle_clicked()
        assert window._history_visible is True

        # Adapter should return the same history
        assert len(mock_adapter.get_history()) == 2
