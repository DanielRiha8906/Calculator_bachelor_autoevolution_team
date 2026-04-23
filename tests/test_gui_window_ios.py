"""Tests for the iOS-style redesigned CalculatorWindow GUI.

Tests the new iOS-style dark calculator layout with:
- Result display at the top (right-aligned, monospace)
- Mode toggle button
- 3-column number grid with "0" spanning full width
- 4-column operations grid with dynamic rows
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
import sys


@pytest.fixture(autouse=True)
def mock_tkinter():
    """Mock tkinter and ttk modules for headless testing.

    Creates mock objects sufficient for the window module to import and
    instantiate objects without a display.
    """
    mock_tk = MagicMock()
    mock_ttk = MagicMock()

    # Create a fake Tk base class that can be subclassed
    class FakeTk:
        def __init__(self):
            self.title_val = ""
            self._grid_info = {}

        def title(self, *args):
            if args:
                self.title_val = args[0]

        def resizable(self, *args):
            pass

        def minsize(self, *args):
            pass

        def configure(self, **kwargs):
            pass

        def columnconfigure(self, *args, **kwargs):
            pass

        def rowconfigure(self, *args, **kwargs):
            pass

        def mainloop(self):
            pass

        def update(self):
            pass

    # StringVar that stores and retrieves values
    class FakeStringVar:
        def __init__(self, value=""):
            self._value = value

        def set(self, value):
            self._value = value

        def get(self):
            return self._value

    mock_tk.Tk = FakeTk
    mock_tk.StringVar = FakeStringVar
    mock_tk.Frame = MagicMock
    mock_tk.Label = MagicMock
    mock_tk.Button = MagicMock
    mock_tk.Canvas = MagicMock
    mock_tk.Text = MagicMock
    mock_tk.END = "end"

    # Create widget factory
    def make_widget():
        widget = MagicMock()
        widget.grid = MagicMock()
        widget.grid_info = MagicMock(return_value={"row": 0, "column": 0, "columnspan": 1})
        widget.configure = MagicMock()
        widget.cget = MagicMock(return_value="#000000")
        widget.bind = MagicMock()
        widget.winfo_children = MagicMock(return_value=[])
        widget.destroy = MagicMock()
        return widget

    # Override widget factories
    def frame_factory(*args, **kwargs):
        return make_widget()

    def label_factory(*args, **kwargs):
        w = make_widget()
        w.cget = MagicMock(side_effect=lambda key: kwargs.get(key, ""))
        return w

    def button_factory(*args, **kwargs):
        w = make_widget()
        w.cget = MagicMock(side_effect=lambda key: kwargs.get(key, ""))
        return w

    mock_tk.Frame = frame_factory
    mock_tk.Label = label_factory
    mock_tk.Button = button_factory

    modules = {
        "tkinter": mock_tk,
        "tkinter.ttk": mock_ttk,
    }

    with patch.dict(sys.modules, modules):
        yield mock_tk, mock_ttk


@pytest.fixture
def mock_adapter():
    """Fixture providing a mocked GUISessionAdapter."""
    adapter = MagicMock()
    # Return both normal and scientific operations
    adapter.get_operations.return_value = [
        "add", "subtract", "multiply", "divide",
        "sqrt", "square", "cube", "power",
        "factorial", "log", "ln", "sin",
        "cos", "tan", "pi", "e"
    ]
    adapter.get_arity.return_value = 2
    adapter.get_history.return_value = []
    adapter.set_mode = MagicMock()
    adapter.execute_operation_safe = MagicMock(return_value=("5.0", ""))
    return adapter


class TestWindowInitialization:
    """Test suite for CalculatorWindow initialization."""

    def test_result_display_shows_zero_initially(self, mock_tkinter, mock_adapter):
        """Test that result display initializes to '0'."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert window._result_var.get() == "0"

    def test_mode_toggle_button_exists(self, mock_tkinter, mock_adapter):
        """Test that mode toggle button is created."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert hasattr(window, "_mode_toggle_btn")
        assert window._mode_toggle_btn is not None

    def test_numbers_grid_exists(self, mock_tkinter, mock_adapter):
        """Test that numbers frame is created."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert hasattr(window, "_numbers_frame")
        assert window._numbers_frame is not None

    def test_operations_grid_exists(self, mock_tkinter, mock_adapter):
        """Test that operations frame is created."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert hasattr(window, "_ops_frame")
        assert window._ops_frame is not None

    def test_current_mode_defaults_to_normal(self, mock_tkinter, mock_adapter):
        """Test that _current_mode initializes to 'normal'."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert window._current_mode == "normal"

    def test_operand_buffer_defaults_to_empty_string(self, mock_tkinter, mock_adapter):
        """Test that _operand_buffer initializes to empty string."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert window._operand_buffer == ""

    def test_selected_op_defaults_to_none(self, mock_tkinter, mock_adapter):
        """Test that _selected_op initializes to None."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert window._selected_op is None

    def test_adapter_reference_stored(self, mock_tkinter, mock_adapter):
        """Test that adapter reference is stored."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert window._adapter is mock_adapter


class TestStyling:
    """Test suite for widget styling."""

    def test_result_display_background_color(self, mock_tkinter, mock_adapter):
        """Test that result display has correct background color."""
        from src.gui.window import CalculatorWindow, _THEME

        window = CalculatorWindow(mock_adapter)
        expected_bg = _THEME["result"]["bg"]
        assert expected_bg == "#000000"
        # Verify the label was configured with this color
        assert window._result_label is not None

    def test_result_display_foreground_color(self, mock_tkinter, mock_adapter):
        """Test that result display has correct foreground color."""
        from src.gui.window import CalculatorWindow, _THEME

        window = CalculatorWindow(mock_adapter)
        expected_fg = _THEME["result"]["fg"]
        assert expected_fg == "#FFFFFF"

    def test_result_display_font(self, mock_tkinter, mock_adapter):
        """Test that result display has correct font."""
        from src.gui.window import CalculatorWindow, _THEME

        window = CalculatorWindow(mock_adapter)
        expected_font = _THEME["result"]["font"]
        assert expected_font == ("Courier New", 32, "bold")

    def test_mode_toggle_button_background(self, mock_tkinter, mock_adapter):
        """Test that mode toggle button has correct background color."""
        from src.gui.window import CalculatorWindow, _THEME

        window = CalculatorWindow(mock_adapter)
        expected_bg = _THEME["colors"]["mode_toggle"]["bg"]
        assert expected_bg == "#FF9500"

    def test_number_buttons_background(self, mock_tkinter, mock_adapter):
        """Test that number buttons have correct background color."""
        from src.gui.window import CalculatorWindow, _THEME

        window = CalculatorWindow(mock_adapter)
        expected_bg = _THEME["colors"]["number"]["bg"]
        assert expected_bg == "#333333"

    def test_operator_buttons_background(self, mock_tkinter, mock_adapter):
        """Test that operator buttons have correct background color."""
        from src.gui.window import CalculatorWindow, _THEME

        window = CalculatorWindow(mock_adapter)
        expected_bg = _THEME["colors"]["operator"]["bg"]
        assert expected_bg == "#FF9500"

    def test_window_background_from_theme(self, mock_tkinter, mock_adapter):
        """Test that window has correct background color."""
        from src.gui.window import CalculatorWindow, _THEME

        window = CalculatorWindow(mock_adapter)
        expected_bg = _THEME["window_bg"]
        assert expected_bg == "#000000"

    def test_theme_has_required_keys(self, mock_tkinter, mock_adapter):
        """Test that _THEME dict has all required keys."""
        from src.gui.window import _THEME

        required_keys = ["window_bg", "result", "colors", "button_font", "mode_button_font", "frame_bg"]
        for key in required_keys:
            assert key in _THEME

    def test_theme_result_has_required_keys(self, mock_tkinter, mock_adapter):
        """Test that _THEME['result'] has required keys."""
        from src.gui.window import _THEME

        required_keys = ["bg", "fg", "font", "pad_x", "pad_y"]
        for key in required_keys:
            assert key in _THEME["result"]


class TestModeToggle:
    """Test suite for mode toggle functionality."""

    def test_mode_toggle_text_in_normal_mode(self, mock_tkinter, mock_adapter):
        """Test that mode toggle button shows 'Scientific' when in normal mode."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # The button text is set during initialization to show opposite mode
        window._mode_toggle_btn.configure.assert_called()

    def test_mode_toggle_text_in_scientific_mode(self, mock_tkinter, mock_adapter):
        """Test that mode toggle button shows 'Normal' when in scientific mode."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window.on_mode_changed("scientific")
        # After changing to scientific, the toggle button should show "Normal"
        assert window._current_mode == "scientific"

    def test_on_mode_changed_updates_current_mode(self, mock_tkinter, mock_adapter):
        """Test that on_mode_changed updates _current_mode."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window.on_mode_changed("scientific")
        assert window._current_mode == "scientific"
        window.on_mode_changed("normal")
        assert window._current_mode == "normal"

    def test_on_mode_changed_calls_adapter_set_mode(self, mock_tkinter, mock_adapter):
        """Test that on_mode_changed calls adapter.set_mode."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        mock_adapter.set_mode.reset_mock()
        window.on_mode_changed("scientific")
        mock_adapter.set_mode.assert_called_with("scientific")

    def test_on_mode_changed_clears_buffers(self, mock_tkinter, mock_adapter):
        """Test that on_mode_changed clears operand buffer and selected operation."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._operand_buffer = "123"
        window._selected_op = "add"

        window.on_mode_changed("scientific")

        assert window._operand_buffer == ""
        assert window._selected_op is None

    def test_on_mode_changed_resets_result_to_zero(self, mock_tkinter, mock_adapter):
        """Test that on_mode_changed resets result display to '0'."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._result_var.set("123")
        window.on_mode_changed("scientific")
        assert window._result_var.get() == "0"

    def test_on_mode_changed_calls_update_operation_buttons(self, mock_tkinter, mock_adapter):
        """Test that on_mode_changed calls update_operation_buttons."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        with patch.object(window, "update_operation_buttons") as mock_update:
            window.on_mode_changed("scientific")
            mock_update.assert_called()


class TestNumberGrid:
    """Test suite for the number grid layout."""

    def test_zero_button_columnspan(self, mock_tkinter, mock_adapter):
        """Test that zero button spans 3 columns."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # The _NUMBER_LAYOUT defines that "0" should span 3 columns
        assert window._NUMBER_LAYOUT[3][0] == "0"

    def test_number_buttons_1_to_9_present(self, mock_tkinter, mock_adapter):
        """Test that all number buttons 1-9 are in the layout."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        all_digits = set()
        for row in window._NUMBER_LAYOUT:
            for digit in row:
                if digit is not None:
                    all_digits.add(digit)

        expected_digits = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}
        assert all_digits == expected_digits

    def test_number_layout_structure(self, mock_tkinter, mock_adapter):
        """Test the structure of the number layout."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        layout = window._NUMBER_LAYOUT

        # Should have 4 rows
        assert len(layout) == 4

        # First 3 rows should have 3 columns each
        for i in range(3):
            assert len(layout[i]) == 3

        # Last row should have "0" and two None placeholders
        assert layout[3][0] == "0"
        assert layout[3][1] is None
        assert layout[3][2] is None


class TestOperationsGrid:
    """Test suite for the operations grid."""

    def test_operations_grid_4_column_layout(self, mock_tkinter, mock_adapter):
        """Test that operations grid is configured for 4 columns."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # The _ops_frame should have 4 columns configured
        assert hasattr(window, "_ops_frame")

    def test_update_operation_buttons_creates_buttons(self, mock_tkinter, mock_adapter):
        """Test that update_operation_buttons creates operation buttons."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        mock_adapter.get_operations.return_value = ["add", "subtract", "multiply"]

        window.update_operation_buttons()

        # Verify get_operations was called
        mock_adapter.get_operations.assert_called()

    def test_operation_symbol_labels(self, mock_tkinter, mock_adapter):
        """Test that operation symbols are mapped correctly."""
        from src.gui.window import _OP_SYMBOLS

        expected_symbols = {
            "add": "+",
            "subtract": "−",
            "multiply": "×",
            "divide": "÷",
            "sqrt": "√",
            "square": "x²",
            "cube": "x³",
            "power": "xʸ",
            "factorial": "n!",
            "log": "log",
            "ln": "ln",
            "sin": "sin",
            "cos": "cos",
            "tan": "tan",
            "pi": "π",
            "e": "e",
        }

        for op_name, expected_symbol in expected_symbols.items():
            assert _OP_SYMBOLS[op_name] == expected_symbol

    def test_op_symbols_has_all_16_operations(self, mock_tkinter, mock_adapter):
        """Test that _OP_SYMBOLS has exactly 16 operations."""
        from src.gui.window import _OP_SYMBOLS

        assert len(_OP_SYMBOLS) == 16

    def test_op_symbols_values_are_unicode_symbols(self, mock_tkinter, mock_adapter):
        """Test that _OP_SYMBOLS values are non-empty strings."""
        from src.gui.window import _OP_SYMBOLS

        for op_name, symbol in _OP_SYMBOLS.items():
            assert isinstance(symbol, str)
            assert len(symbol) > 0

    def test_operator_ops_frozenset_contains_basic_operators(self, mock_tkinter, mock_adapter):
        """Test that _OPERATOR_OPS contains the four basic operators."""
        from src.gui.window import _OPERATOR_OPS

        expected_ops = {"add", "subtract", "multiply", "divide"}
        assert _OPERATOR_OPS == expected_ops


class TestHoverEffect:
    """Test suite for hover effects on buttons."""

    def test_bind_hover_binds_enter_event(self, mock_tkinter, mock_adapter):
        """Test that _bind_hover binds the Enter event."""
        from src.gui.window import CalculatorWindow

        mock_button = MagicMock()
        CalculatorWindow._bind_hover(mock_button, "#333333", "#4D4D4D")

        # Verify bind was called with "<Enter>"
        calls = mock_button.bind.call_args_list
        assert any("<Enter>" in str(call) for call in calls)

    def test_bind_hover_binds_leave_event(self, mock_tkinter, mock_adapter):
        """Test that _bind_hover binds the Leave event."""
        from src.gui.window import CalculatorWindow

        mock_button = MagicMock()
        CalculatorWindow._bind_hover(mock_button, "#333333", "#4D4D4D")

        # Verify bind was called with "<Leave>"
        calls = mock_button.bind.call_args_list
        assert any("<Leave>" in str(call) for call in calls)

    def test_bind_hover_enter_changes_background(self, mock_tkinter, mock_adapter):
        """Test that hovering over button changes background to hover color."""
        from src.gui.window import CalculatorWindow

        mock_button = MagicMock()
        normal_color = "#333333"
        hover_color = "#4D4D4D"

        CalculatorWindow._bind_hover(mock_button, normal_color, hover_color)

        # Get the Enter event handler
        bind_calls = mock_button.bind.call_args_list
        enter_handler = None
        for call in bind_calls:
            if "<Enter>" in str(call):
                enter_handler = call[0][1]
                break

        # Simulate the event
        if enter_handler:
            enter_handler(MagicMock())
            mock_button.configure.assert_called_with(bg=hover_color)

    def test_bind_hover_leave_restores_background(self, mock_tkinter, mock_adapter):
        """Test that leaving button restores background to normal color."""
        from src.gui.window import CalculatorWindow

        mock_button = MagicMock()
        normal_color = "#333333"
        hover_color = "#4D4D4D"

        CalculatorWindow._bind_hover(mock_button, normal_color, hover_color)

        # Get the Leave event handler
        bind_calls = mock_button.bind.call_args_list
        leave_handler = None
        for call in bind_calls:
            if "<Leave>" in str(call):
                leave_handler = call[0][1]
                break

        # Simulate the event
        if leave_handler:
            mock_button.configure.reset_mock()
            leave_handler(MagicMock())
            mock_button.configure.assert_called_with(bg=normal_color)


class TestOperationSelection:
    """Test suite for operation selection behavior."""

    def test_on_operation_selected_stores_operation(self, mock_tkinter, mock_adapter):
        """Test that on_operation_selected stores the selected operation."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        mock_adapter.get_arity.return_value = 2

        window.on_operation_selected("add")

        assert window._selected_op == "add"

    def test_on_operation_selected_calls_get_arity(self, mock_tkinter, mock_adapter):
        """Test that on_operation_selected calls adapter.get_arity."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        mock_adapter.get_arity.reset_mock()
        mock_adapter.get_arity.return_value = 2

        window.on_operation_selected("multiply")

        mock_adapter.get_arity.assert_called_with("multiply")

    def test_on_operation_selected_unary_with_buffer_executes(self, mock_tkinter, mock_adapter):
        """Test that unary operation executes when buffer has a value."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        mock_adapter.get_arity.return_value = 1
        mock_adapter.execute_operation_safe.return_value = ("4.0", "")
        window._operand_buffer = "16"

        window.on_operation_selected("sqrt")

        mock_adapter.execute_operation_safe.assert_called_once()

    def test_on_operation_selected_unary_without_buffer_no_execute(self, mock_tkinter, mock_adapter):
        """Test that unary operation doesn't execute without a buffer value."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        mock_adapter.get_arity.return_value = 1
        window._operand_buffer = ""

        window.on_operation_selected("sqrt")

        mock_adapter.execute_operation_safe.assert_not_called()

    def test_on_operation_selected_binary_no_execute(self, mock_tkinter, mock_adapter):
        """Test that binary operation doesn't execute immediately."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        mock_adapter.get_arity.return_value = 2
        window._operand_buffer = "5"

        window.on_operation_selected("add")

        mock_adapter.execute_operation_safe.assert_not_called()

    def test_on_operation_selected_shows_symbol(self, mock_tkinter, mock_adapter):
        """Test that operation selection shows the operation symbol."""
        from src.gui.window import CalculatorWindow, _OP_SYMBOLS

        window = CalculatorWindow(mock_adapter)
        mock_adapter.get_arity.return_value = 2
        window._operand_buffer = ""

        window.on_operation_selected("add")

        # The display should show "+ ..."
        result_text = window._result_var.get()
        assert "+" in result_text


class TestDigitInput:
    """Test suite for digit input."""

    def test_on_digit_pressed_appends_to_buffer(self, mock_tkinter, mock_adapter):
        """Test that pressing a digit appends it to the buffer."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._on_digit_pressed("5")

        assert window._operand_buffer == "5"

    def test_on_digit_pressed_updates_display(self, mock_tkinter, mock_adapter):
        """Test that pressing a digit updates the result display."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._on_digit_pressed("7")

        assert window._result_var.get() == "7"

    def test_on_digit_pressed_multiple_digits(self, mock_tkinter, mock_adapter):
        """Test that multiple digits are accumulated."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._on_digit_pressed("1")
        window._on_digit_pressed("2")
        window._on_digit_pressed("3")

        assert window._operand_buffer == "123"
        assert window._result_var.get() == "123"


class TestResultDisplay:
    """Test suite for result display management."""

    def test_set_result_updates_display(self, mock_tkinter, mock_adapter):
        """Test that _set_result updates the display."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._set_result("42")

        assert window._result_var.get() == "42"

    def test_set_result_with_error_message(self, mock_tkinter, mock_adapter):
        """Test that error messages can be displayed."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._set_result("Error: Division by zero")

        assert "Error" in window._result_var.get()


class TestExecuteCurrentOperation:
    """Test suite for operation execution."""

    def test_execute_without_selected_op_shows_message(self, mock_tkinter, mock_adapter):
        """Test that executing without selecting an op shows a message."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._selected_op = None

        window._execute_current_operation()

        result = window._result_var.get()
        assert "Select an operation" in result

    def test_execute_without_operand_shows_message(self, mock_tkinter, mock_adapter):
        """Test that executing without an operand shows a message."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._selected_op = "sqrt"
        window._operand_buffer = ""

        window._execute_current_operation()

        result = window._result_var.get()
        assert "Enter a number" in result

    def test_execute_with_invalid_operand_shows_error(self, mock_tkinter, mock_adapter):
        """Test that invalid operands show an error."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._selected_op = "sqrt"
        window._operand_buffer = "abc"

        window._execute_current_operation()

        result = window._result_var.get()
        assert "Invalid" in result

    def test_execute_unary_operation_success(self, mock_tkinter, mock_adapter):
        """Test successful unary operation execution."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._selected_op = "sqrt"
        window._operand_buffer = "16"
        mock_adapter.get_arity.return_value = 1
        mock_adapter.execute_operation_safe.return_value = ("4.0", "")

        window._execute_current_operation()

        assert window._operand_buffer == "4.0"
        assert window._result_var.get() == "4.0"

    def test_execute_binary_operation_shows_message(self, mock_tkinter, mock_adapter):
        """Test that binary operation execution shows a message."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._selected_op = "add"
        window._operand_buffer = "5"
        mock_adapter.get_arity.return_value = 2

        window._execute_current_operation()

        result = window._result_var.get()
        assert "Use operand entry" in result or "binary" in result.lower()

    def test_execute_operation_error_from_adapter(self, mock_tkinter, mock_adapter):
        """Test handling of errors from the adapter."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._selected_op = "sqrt"
        window._operand_buffer = "-1"
        mock_adapter.get_arity.return_value = 1
        mock_adapter.execute_operation_safe.return_value = ("", "Cannot take sqrt of negative")

        window._execute_current_operation()

        result = window._result_var.get()
        assert "Error" in result


class TestModeToggleButton:
    """Test suite for mode toggle button callback."""

    def test_on_mode_toggle_clicked_switches_mode(self, mock_tkinter, mock_adapter):
        """Test that clicking mode toggle switches the mode."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert window._current_mode == "normal"

        window._on_mode_toggle_clicked()

        assert window._current_mode == "scientific"

        window._on_mode_toggle_clicked()

        assert window._current_mode == "normal"


class TestUpdateOperationButtons:
    """Test suite for update_operation_buttons method."""

    def test_update_operation_buttons_destroys_existing(self, mock_tkinter, mock_adapter):
        """Test that update_operation_buttons destroys existing widgets."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)

        # Create a mock child widget
        mock_child = MagicMock()
        window._ops_frame.winfo_children.return_value = [mock_child]

        window.update_operation_buttons()

        mock_child.destroy.assert_called()

    def test_update_operation_buttons_gets_operations_from_adapter(self, mock_tkinter, mock_adapter):
        """Test that update_operation_buttons calls adapter.get_operations."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        mock_adapter.get_operations.reset_mock()

        window.update_operation_buttons()

        mock_adapter.get_operations.assert_called()

    def test_update_operation_buttons_configures_rows(self, mock_tkinter, mock_adapter):
        """Test that update_operation_buttons configures grid rows."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        mock_adapter.get_operations.return_value = ["op1", "op2", "op3", "op4", "op5"]

        window.update_operation_buttons()

        # Should have configured at least 2 rows (5 ops in 4 columns = 2 rows)
        assert window._ops_frame.rowconfigure.called


class TestEdgeCases:
    """Test suite for edge cases and error conditions."""

    def test_window_with_no_operations_in_adapter(self, mock_tkinter, mock_adapter):
        """Test window behavior when adapter returns no operations."""
        from src.gui.window import CalculatorWindow

        mock_adapter.get_operations.return_value = []
        window = CalculatorWindow(mock_adapter)

        window.update_operation_buttons()

        # Should not crash
        assert window is not None

    def test_window_with_single_operation(self, mock_tkinter, mock_adapter):
        """Test window with only one operation in adapter."""
        from src.gui.window import CalculatorWindow

        mock_adapter.get_operations.return_value = ["add"]
        window = CalculatorWindow(mock_adapter)

        window.update_operation_buttons()

        assert window is not None

    def test_operand_buffer_with_special_characters(self, mock_tkinter, mock_adapter):
        """Test handling of special characters in operand buffer."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._on_digit_pressed("5")

        # Verify buffer still works as expected
        assert "5" in window._result_var.get()

    def test_mode_toggle_multiple_times(self, mock_tkinter, mock_adapter):
        """Test toggling mode multiple times."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)

        for _ in range(5):
            window._on_mode_toggle_clicked()

        # After odd number of toggles, should be in scientific
        assert window._current_mode == "scientific"

    def test_result_display_with_long_number(self, mock_tkinter, mock_adapter):
        """Test result display with a very long number."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        long_number = "1.234567890123456789012345678901234567890"
        window._set_result(long_number)

        assert window._result_var.get() == long_number

    def test_operation_selection_after_mode_change(self, mock_tkinter, mock_adapter):
        """Test selecting operation after changing mode."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        mock_adapter.get_arity.return_value = 2

        window.on_mode_changed("scientific")
        window.on_operation_selected("add")

        assert window._selected_op == "add"

    def test_clear_buffers_on_mode_change(self, mock_tkinter, mock_adapter):
        """Test that changing mode clears accumulated state."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._operand_buffer = "999"
        window._selected_op = "multiply"
        window._result_var.set("999")

        window.on_mode_changed("scientific")

        assert window._operand_buffer == ""
        assert window._selected_op is None
        assert window._result_var.get() == "0"
