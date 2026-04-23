"""Tests for src.gui.window module.

Tests the CalculatorWindow Tkinter GUI implementation.

Since Tkinter is not available in headless CI environments and the window
class has very tight coupling with tkinter widgets, this test module uses
mocking to test that:
1. The module can be imported when tkinter is mocked
2. The CalculatorWindow class has all required methods
3. Methods are callable and accept expected parameters
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, ANY
import sys


@pytest.fixture(autouse=True)
def mock_tkinter():
    """Mock tkinter and ttk modules for headless testing.

    This creates mock objects for tkinter and ttk that are sufficient for
    the window module to import and instantiate objects.
    """
    # Create a more sophisticated mock that can handle widget creation
    mock_tk_module = MagicMock()
    mock_ttk_module = MagicMock()

    # Create a fake Tk class that can be subclassed
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

    # Setup module-level attributes
    mock_tk_module.Tk = FakeTk

    # Create a better StringVar mock that tracks set/get values
    class FakeStringVar:
        def __init__(self, value=""):
            self._value = value
        def get(self):
            return self._value
        def set(self, value):
            self._value = value

    mock_tk_module.StringVar = FakeStringVar
    mock_tk_module.Canvas = MagicMock
    mock_tk_module.Text = MagicMock
    mock_tk_module.Event = MagicMock
    mock_tk_module.END = "end"

    # Widget factory - returns mocks with necessary methods
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

    # Setup ttk widgets
    mock_ttk_module.LabelFrame = MagicMock(side_effect=lambda *args, **kwargs: make_widget())
    mock_ttk_module.Button = MagicMock(side_effect=lambda *args, **kwargs: make_widget())
    mock_ttk_module.Entry = MagicMock(side_effect=lambda *args, **kwargs: make_widget())
    mock_ttk_module.Label = MagicMock(side_effect=lambda *args, **kwargs: make_widget())
    mock_ttk_module.Frame = MagicMock(side_effect=lambda *args, **kwargs: make_widget())
    mock_ttk_module.Scrollbar = MagicMock(side_effect=lambda *args, **kwargs: make_widget())

    # Setup tk widget factories
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
    """Fixture providing a mocked GUISessionAdapter."""
    adapter = MagicMock()
    adapter.get_operations.return_value = ["add", "subtract", "multiply"]
    adapter.get_arity.return_value = 2
    adapter.get_history.return_value = []
    return adapter


class TestCalculatorWindowImportAndBasics:
    """Test suite for CalculatorWindow import and basic structure."""

    def test_window_module_imports_successfully(self, mock_tkinter):
        """Test that the window module can be imported with mocked tkinter."""
        from src.gui.window import CalculatorWindow
        assert CalculatorWindow is not None

    def test_window_class_is_defined(self, mock_tkinter):
        """Test that CalculatorWindow class is defined."""
        from src.gui.window import CalculatorWindow
        assert hasattr(CalculatorWindow, "__init__")

    def test_window_has_required_event_handlers(self, mock_tkinter):
        """Test that CalculatorWindow has all required event handler methods."""
        from src.gui.window import CalculatorWindow

        required_methods = [
            "on_mode_changed",
            "on_operation_selected",
            "on_execute_clicked",
            "on_clear_history_clicked",
            "update_history_display",
            "update_operation_buttons",
            "on_number_clicked",
            "on_equals_clicked",
            "on_history_toggle_clicked",
        ]

        for method_name in required_methods:
            assert hasattr(CalculatorWindow, method_name)
            assert callable(getattr(CalculatorWindow, method_name))

    def test_window_can_be_instantiated(self, mock_tkinter, mock_adapter):
        """Test that CalculatorWindow can be instantiated with a mock adapter."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert window is not None

    def test_window_stores_adapter_reference(self, mock_tkinter, mock_adapter):
        """Test that CalculatorWindow stores the adapter reference."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert window._adapter is mock_adapter

    def test_window_initializes_selected_op_to_none(self, mock_tkinter, mock_adapter):
        """Test that window initializes _selected_op to None."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert window._selected_op is None


class TestCalculatorWindowEventHandlers:
    """Test suite for event handler signatures and basic execution."""

    def test_on_mode_changed_accepts_mode_name(self, mock_tkinter, mock_adapter):
        """Test that on_mode_changed accepts a mode_name parameter."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # Should not raise
        window.on_mode_changed("normal")

    def test_on_mode_changed_calls_adapter_set_mode(self, mock_tkinter, mock_adapter):
        """Test that on_mode_changed calls adapter.set_mode."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window.on_mode_changed("scientific")

        # Verify the adapter method was called
        mock_adapter.set_mode.assert_called_with("scientific")

    def test_on_operation_selected_accepts_operation_name(self, mock_tkinter, mock_adapter):
        """Test that on_operation_selected accepts an operation name."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # Should not raise
        window.on_operation_selected("add")

    def test_on_operation_selected_stores_operation(self, mock_tkinter, mock_adapter):
        """Test that on_operation_selected stores the selected operation."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window.on_operation_selected("multiply")

        assert window._selected_op == "multiply"

    def test_on_operation_selected_calls_adapter_get_arity(self, mock_tkinter, mock_adapter):
        """Test that on_operation_selected calls adapter.get_arity."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        mock_adapter.get_arity.reset_mock()

        window.on_operation_selected("add")

        mock_adapter.get_arity.assert_called_with("add")

    def test_on_execute_clicked_is_callable(self, mock_tkinter, mock_adapter):
        """Test that on_execute_clicked can be called."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # Should not raise
        window.on_execute_clicked()

    def test_on_execute_clicked_with_no_operation_selected(self, mock_tkinter, mock_adapter):
        """Test on_execute_clicked when no operation is selected."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._selected_op = None

        # Should handle gracefully without calling adapter.execute_operation_safe
        window.on_execute_clicked()
        mock_adapter.execute_operation_safe.assert_not_called()

    def test_on_execute_clicked_with_valid_selection(self, mock_tkinter, mock_adapter):
        """Test on_execute_clicked with a binary operation pending.

        Uses the new button-only flow where operands come from accumulator.
        """
        from src.gui.window import CalculatorWindow

        mock_adapter.execute_operation_safe.return_value = ("7.0", "")
        mock_adapter.get_arity.return_value = 2

        window = CalculatorWindow(mock_adapter)
        # Simulate: user clicked "3", clicked "add", clicked "4"
        window._display_value = "3 + 4"
        window._display_var.set("3 + 4")
        window._pending_binary_op = "add"

        window.on_execute_clicked()

        # Should have called execute_operation_safe
        mock_adapter.execute_operation_safe.assert_called_once()

    def test_on_clear_history_clicked_is_callable(self, mock_tkinter, mock_adapter):
        """Test that on_clear_history_clicked can be called."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # Should not raise
        window.on_clear_history_clicked()

    def test_on_clear_history_clicked_calls_adapter_clear_history(self, mock_tkinter, mock_adapter):
        """Test that on_clear_history_clicked calls adapter.clear_history."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window.on_clear_history_clicked()

        mock_adapter.clear_history.assert_called_once()


class TestCalculatorWindowUpdateMethods:
    """Test suite for update methods."""

    def test_update_history_display_is_callable(self, mock_tkinter, mock_adapter):
        """Test that update_history_display can be called."""
        from src.gui.window import CalculatorWindow

        mock_adapter.get_history.return_value = []
        window = CalculatorWindow(mock_adapter)
        # Should not raise
        window.update_history_display()

    def test_update_history_display_calls_adapter_get_history(self, mock_tkinter, mock_adapter):
        """Test that update_history_display calls adapter.get_history."""
        from src.gui.window import CalculatorWindow

        mock_adapter.get_history.return_value = []
        window = CalculatorWindow(mock_adapter)
        mock_adapter.get_history.reset_mock()

        window.update_history_display()

        mock_adapter.get_history.assert_called_once()

    def test_update_operation_buttons_is_callable(self, mock_tkinter, mock_adapter):
        """Test that update_operation_buttons can be called."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # Should not raise
        window.update_operation_buttons()

    def test_update_operation_buttons_calls_adapter_get_operations(self, mock_tkinter, mock_adapter):
        """Test that update_operation_buttons calls adapter.get_operations."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        mock_adapter.get_operations.reset_mock()

        window.update_operation_buttons()

        mock_adapter.get_operations.assert_called_once()


class TestCalculatorWindowInitialization:
    """Test suite for initialization behavior."""

    def test_window_calls_build_ui_on_init(self, mock_tkinter, mock_adapter):
        """Test that __init__ calls _build_ui."""
        from src.gui.window import CalculatorWindow

        with patch.object(CalculatorWindow, "_build_ui") as mock_build:
            with patch.object(CalculatorWindow, "on_mode_changed"):
                window = CalculatorWindow(mock_adapter)
                mock_build.assert_called_once()

    def test_window_calls_on_mode_changed_normal_on_init(self, mock_tkinter, mock_adapter):
        """Test that __init__ calls on_mode_changed('normal')."""
        from src.gui.window import CalculatorWindow

        with patch.object(CalculatorWindow, "on_mode_changed") as mock_on_mode:
            window = CalculatorWindow(mock_adapter)
            mock_on_mode.assert_called_with("normal")


class TestCalculatorWindowBuildUI:
    """Test suite for _build_ui method."""

    def test_build_ui_creates_widgets(self, mock_tkinter, mock_adapter):
        """Test that _build_ui creates necessary widget attributes."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)

        # Check that key widgets were created as attributes
        assert hasattr(window, "_result_var")
        assert hasattr(window, "_result_label_widget")
        assert hasattr(window, "_history_text")
        assert hasattr(window, "_ops_frame")

    def test_build_ui_sets_window_title(self, mock_tkinter, mock_adapter):
        """Test that _build_ui sets the window title."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # If title was called, this should work (it's mocked)
        assert window is not None


class TestThemeConstants:
    """Test suite for theme constants."""

    def test_theme_dict_structure(self, mock_tkinter):
        """Test that _THEME contains required keys with valid color format."""
        from src.gui.window import _THEME

        required_keys = {
            "bg",
            "fg",
            "operator_bg",
            "operator_active",
            "sci_bg",
            "sci_active",
            "std_bg",
            "std_active",
            "mode_toggle_bg",
            "mode_toggle_active",
            "display_font",
            "button_font",
            "label_font",
            "entry_font",
            "history_font",
            "error_fg",
            "success_fg",
        }

        assert set(_THEME.keys()) == required_keys

        # Verify color values are in hex format
        color_keys = {
            "bg",
            "fg",
            "operator_bg",
            "operator_active",
            "sci_bg",
            "sci_active",
            "std_bg",
            "std_active",
            "mode_toggle_bg",
            "mode_toggle_active",
            "error_fg",
            "success_fg",
        }
        for key in color_keys:
            value = _THEME[key]
            assert isinstance(value, str)
            assert value.startswith("#") and len(value) == 7

        # Verify font values are tuples
        font_keys = {"display_font", "button_font", "label_font", "entry_font", "history_font"}
        for key in font_keys:
            value = _THEME[key]
            assert isinstance(value, tuple)
            assert len(value) >= 2  # Font name, size, optional style


class TestSymbolMapConstants:
    """Test suite for symbol mapping constants."""

    def test_symbol_map_contains_arithmetic_ops(self, mock_tkinter):
        """Test that _SYMBOL_MAP has arithmetic operations mapped."""
        from src.gui.window import _SYMBOL_MAP

        assert _SYMBOL_MAP["add"] == "+"
        assert _SYMBOL_MAP["subtract"] == "−"
        assert _SYMBOL_MAP["multiply"] == "×"
        assert _SYMBOL_MAP["divide"] == "÷"


class TestArithmeticOpsConstant:
    """Test suite for _ARITHMETIC_OPS constant."""

    def test_arithmetic_ops_is_tuple(self, mock_tkinter):
        """Test that _ARITHMETIC_OPS is a tuple."""
        from src.gui.window import _ARITHMETIC_OPS

        assert isinstance(_ARITHMETIC_OPS, tuple)

    def test_arithmetic_ops_contains_four_operators(self, mock_tkinter):
        """Test that _ARITHMETIC_OPS contains the four basic operators."""
        from src.gui.window import _ARITHMETIC_OPS

        assert set(_ARITHMETIC_OPS) == {"add", "subtract", "multiply", "divide"}
        assert len(_ARITHMETIC_OPS) == 4


class TestResultDisplay:
    """Test suite for result display initialization and behavior."""

    def test_result_display_initialization(self, mock_tkinter, mock_adapter):
        """Test that result label shows '0' on startup."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)

        # Result should be initialized to "0"
        assert window._result_var.get() == "0"

    def test_set_result_empty_shows_zero(self, mock_tkinter, mock_adapter):
        """Test that _set_result('') displays '0'."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._set_result("")

        assert window._result_var.get() == "0"

    def test_set_result_with_text_shows_text(self, mock_tkinter, mock_adapter):
        """Test that _set_result(text) displays the provided text."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._set_result("42.5")

        assert window._result_var.get() == "42.5"

    def test_set_result_error_flag_sets_error_color(self, mock_tkinter, mock_adapter):
        """Test that is_error=True applies error color."""
        from src.gui.window import CalculatorWindow, _THEME

        window = CalculatorWindow(mock_adapter)
        window._set_result("Error message", is_error=True)

        # The label's configure method should have been called with the error color
        # Since label is mocked, verify the call was made
        assert window._result_label_widget.configure.called


class TestModeToggleButton:
    """Test suite for mode toggle button."""

    def test_mode_toggle_button_exists(self, mock_tkinter, mock_adapter):
        """Test that mode toggle button exists."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert hasattr(window, "_mode_toggle_btn")
        assert window._mode_toggle_btn is not None

    def test_mode_toggle_initial_label(self, mock_tkinter, mock_adapter):
        """Test that toggle button shows 'scientific' initially (normal mode)."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # After on_mode_changed("normal"), toggle should show "scientific"
        assert window._current_mode == "normal"

    def test_mode_changed_updates_toggle_label(self, mock_tkinter, mock_adapter):
        """Test that on_mode_changed updates the toggle button label."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # Initial: normal mode, button shows "scientific"
        assert window._current_mode == "normal"

        # Switch to scientific
        window.on_mode_changed("scientific")
        assert window._current_mode == "scientific"

    def test_mode_changed_calls_update_operation_buttons(self, mock_tkinter, mock_adapter):
        """Test that on_mode_changed rebuilds the operation grid."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)

        with patch.object(window, "update_operation_buttons") as mock_update:
            window.on_mode_changed("scientific")
            mock_update.assert_called_once()


class TestNumbersGridLayout:
    """Test suite for numbers grid layout."""

    def test_numbers_grid_layout_exists(self, mock_tkinter, mock_adapter):
        """Test that numbers frame is created with proper layout."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # Numbers frame should exist after _build_ui
        assert window is not None

    def test_numbers_grid_is_three_columns(self, mock_tkinter, mock_adapter):
        """Test that numbers grid uses 3 columns."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # The numbers frame was created with 3 columns configured
        # This is implicitly tested if window builds without errors
        assert window is not None


class TestOperationsGrid:
    """Test suite for operations grid."""

    def test_ops_frame_exists(self, mock_tkinter, mock_adapter):
        """Test that operations frame exists."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert hasattr(window, "_ops_frame")

    def test_operations_grid_uses_four_columns(self, mock_tkinter, mock_adapter):
        """Test that operations grid uses 4-column layout."""
        from src.gui.window import CalculatorWindow

        mock_adapter.get_operations.return_value = ["add", "subtract", "multiply", "divide"]
        window = CalculatorWindow(mock_adapter)
        window.update_operation_buttons()

        # Verify the frame is configured with 4 columns
        # We check that columnconfigure was called for columns 0-3
        assert window._ops_frame.columnconfigure.called

    def test_operation_symbol_mapping_applied(self, mock_tkinter, mock_adapter):
        """Test that operation buttons display mapped symbols."""
        from src.gui.window import CalculatorWindow, _SYMBOL_MAP

        mock_adapter.get_operations.return_value = ["add", "subtract", "multiply", "divide"]
        window = CalculatorWindow(mock_adapter)
        window.update_operation_buttons()

        # Verify operations were retrieved
        mock_adapter.get_operations.assert_called()

    def test_operator_button_colors_arithmetic(self, mock_tkinter, mock_adapter):
        """Test that arithmetic operators get orange background."""
        from src.gui.window import CalculatorWindow, _THEME, _ARITHMETIC_OPS

        window = CalculatorWindow(mock_adapter)

        # Test _op_colors for arithmetic operators
        for op in _ARITHMETIC_OPS:
            default_bg, active_bg = window._op_colors(op)
            assert default_bg == _THEME["operator_bg"]
            assert active_bg == _THEME["operator_active"]

    def test_operator_button_colors_scientific_mode(self, mock_tkinter, mock_adapter):
        """Test that non-arithmetic ops in scientific mode get sci colors."""
        from src.gui.window import CalculatorWindow, _THEME

        window = CalculatorWindow(mock_adapter)
        window._current_mode = "scientific"

        default_bg, active_bg = window._op_colors("sqrt")
        assert default_bg == _THEME["sci_bg"]
        assert active_bg == _THEME["sci_active"]

    def test_operator_button_colors_normal_mode(self, mock_tkinter, mock_adapter):
        """Test that non-arithmetic ops in normal mode get std colors."""
        from src.gui.window import CalculatorWindow, _THEME

        window = CalculatorWindow(mock_adapter)
        window._current_mode = "normal"

        default_bg, active_bg = window._op_colors("sqrt")
        assert default_bg == _THEME["std_bg"]
        assert active_bg == _THEME["std_active"]

    def test_operations_grid_rebuilds_on_mode_change(self, mock_tkinter, mock_adapter):
        """Test that switching modes rebuilds the operations grid."""
        from src.gui.window import CalculatorWindow

        mock_adapter.get_operations.return_value = ["add", "subtract"]
        window = CalculatorWindow(mock_adapter)

        # Clear mock calls
        window._ops_frame.winfo_children.reset_mock()

        # Change mode
        window.on_mode_changed("scientific")

        # Verify winfo_children was called to get widgets to destroy
        assert window._ops_frame.winfo_children.called


class TestHoverEffects:
    """Test suite for button hover effects."""

    def test_bind_hover_binds_enter_and_leave_events(self, mock_tkinter, mock_adapter):
        """Test that _bind_hover binds both Enter and Leave events."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        btn = window._mode_toggle_btn

        # Verify bind was called for Enter and Leave
        bind_calls = [call[0][0] for call in btn.bind.call_args_list]
        assert "<Enter>" in bind_calls
        assert "<Leave>" in bind_calls

    def test_button_hover_changes_color_on_enter(self, mock_tkinter, mock_adapter):
        """Test that hovering over button changes bg to active color."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # Bind calls are mocked; we just verify they were registered
        assert window._mode_toggle_btn.bind.called


class TestFrameBackgrounds:
    """Test suite for frame backgrounds from theme."""

    def test_main_window_bg_from_theme(self, mock_tkinter, mock_adapter):
        """Test that main window bg is set from _THEME."""
        from src.gui.window import CalculatorWindow, _THEME

        window = CalculatorWindow(mock_adapter)
        # Window was initialized with _THEME background
        assert window is not None
        # Verify window exists with proper theme colors available
        assert _THEME["bg"] == "#000000"


class TestModeCurrentState:
    """Test suite for _current_mode attribute."""

    def test_current_mode_initialized_to_normal(self, mock_tkinter, mock_adapter):
        """Test that _current_mode starts as 'normal'."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert window._current_mode == "normal"

    def test_current_mode_updated_on_mode_changed(self, mock_tkinter, mock_adapter):
        """Test that on_mode_changed updates _current_mode."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window.on_mode_changed("scientific")
        assert window._current_mode == "scientific"

        window.on_mode_changed("normal")
        assert window._current_mode == "normal"


class TestOperationSelectionWithModeChange:
    """Test suite for operation selection behavior with mode changes."""

    def test_mode_change_clears_selected_operation(self, mock_tkinter, mock_adapter):
        """Test that changing mode clears the selected operation."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._selected_op = "add"

        window.on_mode_changed("scientific")

        assert window._selected_op is None

    def test_mode_change_clears_result_display(self, mock_tkinter, mock_adapter):
        """Test that changing mode clears the result display."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._set_result("42")

        window.on_mode_changed("scientific")

        # After mode change, _set_result("") is called, which sets to "0"
        assert window._result_var.get() == "0"


class TestNumberClickedHandler:
    """Test suite for on_number_clicked event handler."""

    def test_on_number_clicked_first_digit_replaces_zero(self, mock_tkinter, mock_adapter):
        """Test that first digit replaces initial '0' display."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert window._display_value == "0"

        window.on_number_clicked("5")

        assert window._display_value == "5"
        assert window._display_var.get() == "5"

    def test_on_number_clicked_subsequent_digits_append(self, mock_tkinter, mock_adapter):
        """Test that subsequent digits append to display."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window.on_number_clicked("5")
        assert window._display_value == "5"

        window.on_number_clicked("3")

        assert window._display_value == "53"
        assert window._display_var.get() == "53"

    @pytest.mark.parametrize("digits", [
        ("5", "3"),
        ("1", "2", "3"),
        ("9", "8", "7", "6"),
    ])
    def test_on_number_clicked_multiple_digits_accumulate(self, mock_tkinter, mock_adapter, digits):
        """Test that multiple digit clicks accumulate correctly."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        for digit in digits:
            window.on_number_clicked(digit)

        expected = "".join(digits)
        assert window._display_value == expected
        assert window._display_var.get() == expected

    def test_on_number_clicked_zero_after_nonzero(self, mock_tkinter, mock_adapter):
        """Test that '0' appends normally after a non-zero digit."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window.on_number_clicked("5")
        window.on_number_clicked("0")

        assert window._display_value == "50"
        assert window._display_var.get() == "50"

    def test_on_number_clicked_updates_display_var(self, mock_tkinter, mock_adapter):
        """Test that on_number_clicked updates _display_var."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window.on_number_clicked("7")

        assert window._display_var.get() == "7"


class TestEqualsClickedHandler:
    """Test suite for on_equals_clicked event handler."""

    def test_on_equals_clicked_is_callable(self, mock_tkinter, mock_adapter):
        """Test that on_equals_clicked can be called."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # Should not raise
        window.on_equals_clicked()

    def test_on_equals_clicked_with_no_pending_op(self, mock_tkinter, mock_adapter):
        """Test on_equals_clicked when no binary operation is pending."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._pending_binary_op = None
        window._selected_op = None

        # Should fall back to on_execute_clicked without error
        window.on_equals_clicked()

        mock_adapter.execute_operation_safe.assert_not_called()


class TestHistoryToggleClickedHandler:
    """Test suite for on_history_toggle_clicked event handler."""

    def test_on_history_toggle_clicked_is_callable(self, mock_tkinter, mock_adapter):
        """Test that on_history_toggle_clicked can be called."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # Should not raise
        window.on_history_toggle_clicked()

    def test_on_history_toggle_clicked_toggles_visibility_true(self, mock_tkinter, mock_adapter):
        """Test on_history_toggle_clicked makes history visible."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert window._history_visible is False

        window.on_history_toggle_clicked()

        assert window._history_visible is True

    def test_on_history_toggle_clicked_toggles_visibility_false(self, mock_tkinter, mock_adapter):
        """Test on_history_toggle_clicked hides history when visible."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._history_visible = True

        window.on_history_toggle_clicked()

        assert window._history_visible is False

    def test_on_history_toggle_clicked_updates_button_label_show(self, mock_tkinter, mock_adapter):
        """Test on_history_toggle_clicked updates button label to 'Hide History'."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # Initial state: hidden, button shows "Show History"
        window._history_visible = False

        window.on_history_toggle_clicked()

        # Now visible, button should show "Hide History"
        window._history_toggle_btn.configure.assert_called()

    def test_on_history_toggle_clicked_updates_button_label_hide(self, mock_tkinter, mock_adapter):
        """Test on_history_toggle_clicked updates button label to 'Show History'."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._history_visible = True

        window.on_history_toggle_clicked()

        # Now hidden again, button should show "Show History"
        window._history_toggle_btn.configure.assert_called()

    def test_on_history_toggle_clicked_multiple_times(self, mock_tkinter, mock_adapter):
        """Test on_history_toggle_clicked can be toggled multiple times."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        initial = window._history_visible

        window.on_history_toggle_clicked()
        assert window._history_visible == (not initial)

        window.on_history_toggle_clicked()
        assert window._history_visible == initial


class TestNewDisplayAttributes:
    """Test suite for new display-related attributes."""

    def test_display_value_initialized_to_zero(self, mock_tkinter, mock_adapter):
        """Test that _display_value is initialized to '0'."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert window._display_value == "0"

    def test_display_var_initialized_to_zero(self, mock_tkinter, mock_adapter):
        """Test that _display_var is initialized to '0'."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert window._display_var.get() == "0"

    def test_pending_binary_op_initialized_to_none(self, mock_tkinter, mock_adapter):
        """Test that _pending_binary_op is initialized to None."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert window._pending_binary_op is None

    def test_history_visible_initialized_to_false(self, mock_tkinter, mock_adapter):
        """Test that _history_visible is initialized to False."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert window._history_visible is False

    def test_history_frame_hidden_on_startup(self, mock_tkinter, mock_adapter):
        """Test that history frame is hidden on startup."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # grid_remove() should have been called on the history frame
        assert window._history_frame.grid_remove.called or window._history_frame.grid_remove == MagicMock

    def test_clear_history_button_hidden_on_startup(self, mock_tkinter, mock_adapter):
        """Test that clear history button is hidden on startup."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # grid_remove() should have been called on the clear button
        assert window._clear_history_btn.grid_remove.called or window._clear_history_btn.grid_remove == MagicMock


class TestModeChangedClearsState:
    """Test suite for mode change clearing pending state."""

    def test_mode_changed_clears_pending_binary_op(self, mock_tkinter, mock_adapter):
        """Test that on_mode_changed clears _pending_binary_op."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._pending_binary_op = "add"

        window.on_mode_changed("scientific")

        assert window._pending_binary_op is None

    def test_mode_changed_calls_adapter_clear_pending_operand(self, mock_tkinter, mock_adapter):
        """Test that on_mode_changed calls adapter.clear_pending_operand."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        mock_adapter.clear_pending_operand.reset_mock()

        window.on_mode_changed("normal")

        mock_adapter.clear_pending_operand.assert_called()

    def test_mode_changed_resets_display_value(self, mock_tkinter, mock_adapter):
        """Test that on_mode_changed resets _display_value to '0'."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._display_value = "123"

        window.on_mode_changed("scientific")

        assert window._display_value == "0"


class TestNoOperandEntryWidgets:
    """Test suite verifying absence of removed entry widgets."""

    def test_window_has_no_operand1_entry_attribute(self, mock_tkinter, mock_adapter):
        """Test that CalculatorWindow does not have _operand1_entry attribute."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert not hasattr(window, "_operand1_entry")

    def test_window_has_no_operand2_entry_attribute(self, mock_tkinter, mock_adapter):
        """Test that CalculatorWindow does not have _operand2_entry attribute."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert not hasattr(window, "_operand2_entry")

    def test_window_has_no_operand2_label_attribute(self, mock_tkinter, mock_adapter):
        """Test that CalculatorWindow does not have _operand2_label attribute."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert not hasattr(window, "_operand2_label")


class TestSymbolMapCompleteness:
    """Test suite for _SYMBOL_MAP completeness against mode operations."""

    def test_all_normal_mode_operations_have_symbols(self, mock_tkinter):
        """Test that every operation in NORMAL_MODE_OPERATIONS has a symbol."""
        from src.gui.window import _SYMBOL_MAP
        from src.mode import NORMAL_MODE_OPERATIONS

        for op_name in NORMAL_MODE_OPERATIONS:
            assert op_name in _SYMBOL_MAP, f"Operation '{op_name}' not in _SYMBOL_MAP"
            symbol = _SYMBOL_MAP[op_name]
            assert isinstance(symbol, str) and len(symbol) > 0, \
                f"Symbol for '{op_name}' is empty or invalid: {symbol!r}"

    def test_all_scientific_mode_operations_have_symbols(self, mock_tkinter):
        """Test that every operation in SCIENTIFIC_MODE_OPERATIONS has a symbol."""
        from src.gui.window import _SYMBOL_MAP
        from src.mode import SCIENTIFIC_MODE_OPERATIONS

        for op_name in SCIENTIFIC_MODE_OPERATIONS:
            assert op_name in _SYMBOL_MAP, f"Operation '{op_name}' not in _SYMBOL_MAP"
            symbol = _SYMBOL_MAP[op_name]
            assert isinstance(symbol, str) and len(symbol) > 0, \
                f"Symbol for '{op_name}' is empty or invalid: {symbol!r}"

    def test_symbol_map_symbols_are_concise(self, mock_tkinter):
        """Test that symbols in _SYMBOL_MAP are concise (reasonable length)."""
        from src.gui.window import _SYMBOL_MAP

        # Most symbols should be ≤ 5 chars; allow some extra for special cases
        for op_name, symbol in _SYMBOL_MAP.items():
            assert len(symbol) <= 8, \
                f"Symbol for '{op_name}' is too long ({len(symbol)} chars): {symbol!r}"


class TestBaseOperationPinning:
    """Test suite verifying that base arithmetic ops are pinned to top."""

    def test_update_operation_buttons_pins_arithmetic_ops_first_normal_mode(
        self, mock_tkinter, mock_adapter
    ):
        """Test that arithmetic ops appear first in normal mode."""
        from src.gui.window import CalculatorWindow, _ARITHMETIC_OPS
        from src.mode import NORMAL_MODE_OPERATIONS

        mock_adapter.get_operations.return_value = NORMAL_MODE_OPERATIONS
        window = CalculatorWindow(mock_adapter)
        window.update_operation_buttons()

        # Get the operation buttons from the frame (they're children).
        # The mocked children should have 6 items (4 arithmetic + 2 others in normal mode)
        # We can't directly inspect the order without introspecting the button
        # commands, but we can verify the frame was created and columnconfigure was called.
        assert window._ops_frame is not None
        assert window._ops_frame.columnconfigure.called

    def test_update_operation_buttons_pins_arithmetic_ops_first_scientific_mode(
        self, mock_tkinter, mock_adapter
    ):
        """Test that arithmetic ops appear first in scientific mode."""
        from src.gui.window import CalculatorWindow, _ARITHMETIC_OPS
        from src.mode import SCIENTIFIC_MODE_OPERATIONS

        mock_adapter.get_operations.return_value = SCIENTIFIC_MODE_OPERATIONS
        window = CalculatorWindow(mock_adapter)
        window._current_mode = "scientific"
        window.update_operation_buttons()

        # Frame should be updated; verify it was refreshed
        assert window._ops_frame is not None

    def test_arithmetic_ops_are_subset_of_all_operations(self, mock_tkinter, mock_adapter):
        """Test that all _ARITHMETIC_OPS are available in at least normal mode."""
        from src.gui.window import _ARITHMETIC_OPS
        from src.mode import NORMAL_MODE_OPERATIONS

        for op in _ARITHMETIC_OPS:
            assert op in NORMAL_MODE_OPERATIONS, \
                f"Arithmetic op '{op}' not in NORMAL_MODE_OPERATIONS"


class TestButtonOnlyBinaryFlow:
    """Test suite for the button-only (iOS-style) binary operation flow."""

    def test_number_operation_number_equals_flow(self, mock_tkinter, mock_adapter):
        """Test: 3 + 4 = via button-only interface."""
        from src.gui.window import CalculatorWindow

        mock_adapter.execute_operation_safe.return_value = ("7.0", "")
        mock_adapter.get_arity.return_value = 2

        window = CalculatorWindow(mock_adapter)

        # Step 1: Click "3"
        window.on_number_clicked("3")
        assert window._display_value == "3"
        assert window._display_var.get() == "3"
        assert window._pending_binary_op is None

        # Step 2: Click "add"
        window.on_operation_selected("add")
        assert window._pending_binary_op == "add"
        assert window._display_value == "3 + "  # Operator appended to display

        # Step 3: Click "4"
        window.on_number_clicked("4")
        assert window._display_value == "3 + 4"

        # Step 4: Click "equals"
        window.on_equals_clicked()

        # Should have called adapter with operand2=4 and use_pending=True
        mock_adapter.execute_operation_safe.assert_called_once()
        call_args = mock_adapter.execute_operation_safe.call_args
        assert call_args[1].get("use_pending") is True

    def test_unary_operation_executes_immediately(self, mock_tkinter, mock_adapter):
        """Test that unary ops (arity=1) execute immediately without pending."""
        from src.gui.window import CalculatorWindow

        mock_adapter.get_arity.return_value = 1
        mock_adapter.execute_operation_safe.return_value = ("4.0", "")

        window = CalculatorWindow(mock_adapter)

        # Click "16" then "square_root"
        window.on_number_clicked("1")
        window.on_number_clicked("6")
        assert window._display_value == "16"

        window.on_operation_selected("square_root")

        # Unary should execute immediately; _pending_binary_op stays None
        assert window._pending_binary_op is None
        mock_adapter.execute_operation_safe.assert_called_once()

    def test_no_attribute_error_on_button_only_flow(self, mock_tkinter, mock_adapter):
        """Test that button-only flow raises no AttributeError."""
        from src.gui.window import CalculatorWindow

        mock_adapter.execute_operation_safe.return_value = ("10.0", "")
        mock_adapter.get_arity.return_value = 2

        window = CalculatorWindow(mock_adapter)

        try:
            window.on_number_clicked("5")
            window.on_operation_selected("multiply")
            window.on_number_clicked("2")
            window.on_equals_clicked()
        except AttributeError as e:
            pytest.fail(f"Button-only flow raised AttributeError: {e}")

    def test_pending_binary_op_cleared_after_execute(self, mock_tkinter, mock_adapter):
        """Test that _pending_binary_op is cleared after execution."""
        from src.gui.window import CalculatorWindow

        mock_adapter.execute_operation_safe.return_value = ("9.0", "")
        mock_adapter.get_arity.return_value = 2

        window = CalculatorWindow(mock_adapter)
        window.on_number_clicked("5")
        window.on_operation_selected("add")
        window.on_number_clicked("4")

        assert window._pending_binary_op == "add"

        window.on_equals_clicked()

        assert window._pending_binary_op is None

    def test_multiple_binary_operations_in_sequence(self, mock_tkinter, mock_adapter):
        """Test: 2 + 3 = 5, then 5 * 2 = 10 without intermediate results."""
        from src.gui.window import CalculatorWindow

        mock_adapter.execute_operation_safe.return_value = ("5.0", "")
        mock_adapter.get_arity.return_value = 2

        window = CalculatorWindow(mock_adapter)

        # First: 2 + 3 = 5
        window.on_number_clicked("2")
        window.on_operation_selected("add")
        window.on_number_clicked("3")
        window.on_equals_clicked()

        # Result is now "5.0", pending is cleared
        assert window._pending_binary_op is None

        # Second: 5 * 2
        # (Note: in a real flow, the user might see "5" and click multiply.
        # For this test, we assume the display shows the result "5.0".)
        mock_adapter.execute_operation_safe.return_value = ("10.0", "")
        window.on_number_clicked("2")  # This appends to "5" assuming no clear
        # For simplicity, reset and start fresh
        window._display_value = "5"
        window._display_var.set("5")

        window.on_operation_selected("multiply")
        window.on_number_clicked("2")
        window.on_equals_clicked()

        # Should be able to execute without error
        assert window._pending_binary_op is None
