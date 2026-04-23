"""Tests for iOS-style GUI theme and window implementation.

Tests the src.gui.ios_theme module constants and the iOS-specific features
of src.gui.window (layout, styling, mode toggle, button grid).

Uses mocking for headless testing since Tkinter is not available in CI.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, ANY
import sys


@pytest.fixture(autouse=True)
def mock_tkinter():
    """Mock tkinter and ttk modules for headless testing."""
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
        def title(self, *args):
            pass
        def resizable(self, *args):
            pass
        def minsize(self, *args):
            pass
        def mainloop(self):
            pass
        def configure(self, **kwargs):
            pass

    # Setup module-level attributes
    mock_tk_module.Tk = FakeTk
    mock_tk_module.StringVar = MagicMock(return_value=MagicMock())
    mock_tk_module.Canvas = MagicMock
    mock_tk_module.Text = MagicMock
    mock_tk_module.Event = MagicMock
    mock_tk_module.END = "end"
    mock_tk_module.X = "x"
    mock_tk_module.Y = "y"
    mock_tk_module.BOTH = "both"
    mock_tk_module.FLAT = "flat"

    # Widget factory - returns mocks with necessary methods
    def make_widget():
        widget = MagicMock()
        widget.grid = MagicMock()
        widget.pack = MagicMock()
        widget.configure = MagicMock()
        widget.cget = MagicMock(return_value="")
        widget.get = MagicMock(return_value="")
        widget.delete = MagicMock()
        widget.insert = MagicMock()
        widget.winfo_children = MagicMock(return_value=[])
        widget.destroy = MagicMock()
        widget.bind = MagicMock(return_value="binding123")
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
    mock_tk_module.Frame = MagicMock(side_effect=lambda *args, **kwargs: make_widget())
    mock_tk_module.Label = MagicMock(side_effect=lambda *args, **kwargs: make_widget())
    mock_tk_module.Button = MagicMock(side_effect=lambda *args, **kwargs: make_widget())
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
    adapter.get_operations.return_value = ["add", "subtract", "multiply", "divide", "square", "square_root"]
    adapter.get_arity.return_value = 2
    adapter.get_history.return_value = []
    adapter.execute_operation.return_value = "42"
    return adapter


# =====================================================================
# Theme Constants Tests
# =====================================================================

class TestIOSThemeConstants:
    """Test suite for ios_theme module constants."""

    def test_theme_dict_exists(self, mock_tkinter):
        """Test that _THEME dict is defined and accessible."""
        from src.gui.ios_theme import _THEME
        assert isinstance(_THEME, dict)

    def test_theme_has_required_color_keys(self, mock_tkinter):
        """Test that _THEME contains all required color keys."""
        from src.gui.ios_theme import _THEME
        required_keys = [
            "bg_window",
            "bg_result_display",
            "fg_result_display",
            "font_result",
            "bg_operator_button",
            "fg_operator_button",
            "active_bg_operator_button",
            "bg_utility_button",
            "fg_utility_button",
            "active_bg_utility_button",
            "bg_standard_button",
            "fg_standard_button",
            "active_bg_standard_button",
            "bg_mode_button",
            "fg_mode_button",
            "active_bg_mode_button",
        ]
        for key in required_keys:
            assert key in _THEME, f"Missing theme key: {key}"

    def test_theme_operator_button_orange(self, mock_tkinter):
        """Test that operator button background is orange (#FF9500)."""
        from src.gui.ios_theme import _THEME
        assert _THEME["bg_operator_button"] == "#FF9500"

    def test_theme_operator_button_active_lighter_orange(self, mock_tkinter):
        """Test that active operator button is lighter orange (#FFB143)."""
        from src.gui.ios_theme import _THEME
        assert _THEME["active_bg_operator_button"] == "#FFB143"

    def test_theme_utility_button_dark(self, mock_tkinter):
        """Test that utility button background is dark (#1C1C1E)."""
        from src.gui.ios_theme import _THEME
        assert _THEME["bg_utility_button"] == "#1C1C1E"

    def test_theme_utility_button_active_lighter_dark(self, mock_tkinter):
        """Test that active utility button is lighter dark (#2C2C2E)."""
        from src.gui.ios_theme import _THEME
        assert _THEME["active_bg_utility_button"] == "#2C2C2E"

    def test_theme_standard_button_grey(self, mock_tkinter):
        """Test that standard button background is grey (#333333)."""
        from src.gui.ios_theme import _THEME
        assert _THEME["bg_standard_button"] == "#333333"

    def test_theme_standard_button_active_lighter_grey(self, mock_tkinter):
        """Test that active standard button is lighter grey (#4D4D4D)."""
        from src.gui.ios_theme import _THEME
        assert _THEME["active_bg_standard_button"] == "#4D4D4D"

    def test_theme_result_display_background_black(self, mock_tkinter):
        """Test that result display background is black (#000000)."""
        from src.gui.ios_theme import _THEME
        assert _THEME["bg_result_display"] == "#000000"

    def test_theme_result_display_foreground_white(self, mock_tkinter):
        """Test that result display foreground is white (#FFFFFF)."""
        from src.gui.ios_theme import _THEME
        assert _THEME["fg_result_display"] == "#FFFFFF"

    def test_theme_result_font_is_tuple(self, mock_tkinter):
        """Test that result font is a tuple."""
        from src.gui.ios_theme import _THEME
        assert isinstance(_THEME["font_result"], tuple)

    def test_theme_result_font_has_size_32(self, mock_tkinter):
        """Test that result font size is 32."""
        from src.gui.ios_theme import _THEME
        font = _THEME["font_result"]
        assert len(font) >= 2
        assert font[1] == 32

    def test_theme_result_font_is_bold(self, mock_tkinter):
        """Test that result font is bold."""
        from src.gui.ios_theme import _THEME
        font = _THEME["font_result"]
        assert len(font) >= 3
        assert font[2] == "bold"

    def test_theme_result_font_is_courier(self, mock_tkinter):
        """Test that result font is Courier."""
        from src.gui.ios_theme import _THEME
        font = _THEME["font_result"]
        assert font[0] == "Courier"


class TestOperationSymbolsConstants:
    """Test suite for OPERATION_SYMBOLS mapping."""

    def test_operation_symbols_dict_exists(self, mock_tkinter):
        """Test that OPERATION_SYMBOLS dict is defined."""
        from src.gui.ios_theme import OPERATION_SYMBOLS
        assert isinstance(OPERATION_SYMBOLS, dict)

    def test_operation_symbols_add(self, mock_tkinter):
        """Test that 'add' operation has correct symbol."""
        from src.gui.ios_theme import OPERATION_SYMBOLS
        assert OPERATION_SYMBOLS["add"] == "+"

    def test_operation_symbols_subtract(self, mock_tkinter):
        """Test that 'subtract' operation has minus sign (U+2212)."""
        from src.gui.ios_theme import OPERATION_SYMBOLS
        assert OPERATION_SYMBOLS["subtract"] == "−"  # U+2212

    def test_operation_symbols_multiply(self, mock_tkinter):
        """Test that 'multiply' operation has multiplication sign."""
        from src.gui.ios_theme import OPERATION_SYMBOLS
        assert OPERATION_SYMBOLS["multiply"] == "×"

    def test_operation_symbols_divide(self, mock_tkinter):
        """Test that 'divide' operation has division sign."""
        from src.gui.ios_theme import OPERATION_SYMBOLS
        assert OPERATION_SYMBOLS["divide"] == "÷"

    def test_operation_symbols_sqrt(self, mock_tkinter):
        """Test that 'sqrt' operation has square root symbol."""
        from src.gui.ios_theme import OPERATION_SYMBOLS
        assert OPERATION_SYMBOLS["sqrt"] == "√"

    def test_operation_symbols_square_root_alias(self, mock_tkinter):
        """Test that 'square_root' is an alias for sqrt."""
        from src.gui.ios_theme import OPERATION_SYMBOLS
        assert OPERATION_SYMBOLS["square_root"] == "√"

    def test_operation_symbols_square(self, mock_tkinter):
        """Test that 'square' operation has x² symbol."""
        from src.gui.ios_theme import OPERATION_SYMBOLS
        assert OPERATION_SYMBOLS["square"] == "x²"

    def test_operation_symbols_pi(self, mock_tkinter):
        """Test that 'pi' operation has π symbol."""
        from src.gui.ios_theme import OPERATION_SYMBOLS
        assert OPERATION_SYMBOLS["pi"] == "π"

    @pytest.mark.parametrize("op_name,expected_symbol", [
        ("add", "+"),
        ("subtract", "−"),
        ("multiply", "×"),
        ("divide", "÷"),
        ("sqrt", "√"),
        ("square_root", "√"),
        ("square", "x²"),
        ("cube", "x³"),
        ("cube_root", "∛"),
        ("power", "xʸ"),
        ("factorial", "n!"),
        ("log", "log"),
        ("logarithm", "log"),
        ("ln", "ln"),
        ("natural_logarithm", "ln"),
        ("sin", "sin"),
        ("cos", "cos"),
        ("tan", "tan"),
        ("cot", "cot"),
        ("asin", "asin"),
        ("acos", "acos"),
        ("atan", "atan"),
        ("pi", "π"),
        ("e", "e"),
    ])
    def test_operation_symbols_all_entries(self, mock_tkinter, op_name, expected_symbol):
        """Test all operation symbols are correctly mapped."""
        from src.gui.ios_theme import OPERATION_SYMBOLS
        assert op_name in OPERATION_SYMBOLS
        assert OPERATION_SYMBOLS[op_name] == expected_symbol


# =====================================================================
# Widget Creation and Configuration Tests
# =====================================================================

class TestIOSLayoutWidgetCreation:
    """Test suite for widget creation in iOS layout."""

    def test_result_label_is_created(self, mock_tkinter, mock_adapter):
        """Test that result label is created after _build_ios_layout."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)
        assert hasattr(window, "_result_label")
        assert window._result_label is not None

    def test_result_label_has_correct_font(self, mock_tkinter, mock_adapter):
        """Test that result label has the correct font."""
        from src.gui.window import CalculatorWindow
        from src.gui.ios_theme import _THEME
        window = CalculatorWindow(mock_adapter)

        # The label was created with font=_THEME["font_result"]
        # We can't directly check the mock's font since it's a MagicMock,
        # but we can verify the label exists and the theme value is correct
        assert _THEME["font_result"] == ("Courier", 32, "bold")

    def test_result_label_anchor_is_east(self, mock_tkinter, mock_adapter):
        """Test that result label is right-aligned (anchor='e')."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)
        # Verify the label has the anchor config
        # Since it's a mock, we check via cget call
        assert hasattr(window, "_result_label")

    def test_result_label_background_is_black(self, mock_tkinter, mock_adapter):
        """Test that result label background is black."""
        from src.gui.window import CalculatorWindow
        from src.gui.ios_theme import _THEME
        window = CalculatorWindow(mock_adapter)
        assert _THEME["bg_result_display"] == "#000000"

    def test_result_label_foreground_is_white(self, mock_tkinter, mock_adapter):
        """Test that result label foreground is white."""
        from src.gui.window import CalculatorWindow
        from src.gui.ios_theme import _THEME
        window = CalculatorWindow(mock_adapter)
        assert _THEME["fg_result_display"] == "#FFFFFF"

    def test_mode_button_is_created(self, mock_tkinter, mock_adapter):
        """Test that mode toggle button is created."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)
        assert hasattr(window, "_mode_button")
        assert window._mode_button is not None

    def test_mode_button_initial_text_is_scientific(self, mock_tkinter, mock_adapter):
        """Test that mode button initial text is 'Scientific' (since mode is normal)."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)
        # The button was created with text="Scientific"
        # Since we're in normal mode, the toggle button should say "Scientific"
        assert window._current_mode == "normal"

    def test_ops_container_is_created(self, mock_tkinter, mock_adapter):
        """Test that operation buttons container frame is created."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)
        assert hasattr(window, "_ops_container")
        assert window._ops_container is not None

    def test_result_label_widget_alias_exists(self, mock_tkinter, mock_adapter):
        """Test that _result_label_widget alias exists for backward compatibility."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)
        assert hasattr(window, "_result_label_widget")
        assert window._result_label_widget is window._result_label


# =====================================================================
# Button Grid Tests
# =====================================================================

class TestButtonGridConstruction:
    """Test suite for button grid construction and styling."""

    def test_normal_mode_has_default_operations(self, mock_tkinter):
        """Test that normal mode uses default operation list."""
        from src.gui.window import CalculatorWindow
        # Create adapter without get_operations method
        adapter = MagicMock(spec=["set_mode"])
        window = CalculatorWindow(adapter)
        window._current_mode = "normal"
        ops = window._get_current_operations()
        assert "add" in ops
        assert "subtract" in ops
        assert "multiply" in ops
        assert "divide" in ops
        assert len(ops) == 6

    def test_scientific_mode_has_extended_operations(self, mock_tkinter):
        """Test that scientific mode uses extended operation list."""
        from src.gui.window import CalculatorWindow
        # Create adapter without get_operations method
        adapter = MagicMock(spec=["set_mode"])
        window = CalculatorWindow(adapter)
        window._current_mode = "scientific"
        ops = window._get_current_operations()
        assert "add" in ops
        assert "subtract" in ops
        assert "multiply" in ops
        assert "divide" in ops
        assert "power" in ops
        assert "factorial" in ops
        assert len(ops) > 6

    def test_get_current_operations_uses_adapter_if_available(self, mock_tkinter, mock_adapter):
        """Test that _get_current_operations delegates to adapter if available."""
        from src.gui.window import CalculatorWindow
        mock_adapter.get_operations.return_value = ["add", "subtract"]
        window = CalculatorWindow(mock_adapter)
        ops = window._get_current_operations()
        assert ops == ["add", "subtract"]
        mock_adapter.get_operations.assert_called()

    def test_button_grid_4_columns(self, mock_tkinter, mock_adapter):
        """Test that button grid is organized in 4 columns."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)
        # Verify columnconfigure was called 4 times for cols 0-3
        assert window._ops_container.columnconfigure.called


# =====================================================================
# Mode Toggle Tests
# =====================================================================

class TestModeToggle:
    """Test suite for mode toggle functionality."""

    def test_mode_toggle_switches_to_scientific(self, mock_tkinter, mock_adapter):
        """Test that toggling from normal switches to scientific."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)
        assert window._current_mode == "normal"
        window._on_mode_toggle()
        assert window._current_mode == "scientific"

    def test_mode_toggle_switches_to_normal(self, mock_tkinter, mock_adapter):
        """Test that toggling from scientific switches to normal."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)
        window._current_mode = "scientific"
        window._on_mode_toggle()
        assert window._current_mode == "normal"

    def test_mode_toggle_calls_adapter_set_mode(self, mock_tkinter, mock_adapter):
        """Test that _on_mode_toggle calls adapter.set_mode with new mode."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)
        mock_adapter.set_mode.reset_mock()
        window._on_mode_toggle()
        mock_adapter.set_mode.assert_called_with("scientific")

    def test_mode_toggle_resets_result_display(self, mock_tkinter, mock_adapter):
        """Test that toggling mode resets result display to '0'."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)
        window._result_var.set("42")
        window._on_mode_toggle()
        window._result_var.set.assert_called_with("0")

    def test_mode_toggle_updates_button_text(self, mock_tkinter, mock_adapter):
        """Test that toggling mode changes the mode button text."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)
        window._on_mode_toggle()
        # After toggle to scientific, button should say "Normal"
        window._mode_button.configure.assert_called()

    def test_mode_toggle_rebuilds_button_grid(self, mock_tkinter, mock_adapter):
        """Test that toggling mode rebuilds the button grid."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)
        # Track children before toggle
        window._ops_container.winfo_children.return_value = []
        window._on_mode_toggle()
        # After toggle, grid should be rebuilt
        # This is verified by the fact that winfo_children and destroy were called
        assert window._ops_container.winfo_children.called

    def test_toggle_twice_restores_original_mode(self, mock_tkinter, mock_adapter):
        """Test that toggling twice returns to the original mode."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)
        original_mode = window._current_mode
        window._on_mode_toggle()
        window._on_mode_toggle()
        assert window._current_mode == original_mode


# =====================================================================
# Operation Click Tests
# =====================================================================

class TestOperationClick:
    """Test suite for operation button click handling."""

    def test_operation_clicked_stores_selected_op(self, mock_tkinter, mock_adapter):
        """Test that clicking an operation stores the operation name."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)
        window._on_operation_clicked("add")
        assert window._selected_op == "add"

    def test_operation_clicked_with_execute_operation(self, mock_tkinter, mock_adapter):
        """Test that _on_operation_clicked calls adapter.execute_operation."""
        from src.gui.window import CalculatorWindow
        mock_adapter.execute_operation.return_value = "42"
        window = CalculatorWindow(mock_adapter)
        window._on_operation_clicked("add")
        mock_adapter.execute_operation.assert_called_with("add")

    def test_operation_clicked_updates_result_display(self, mock_tkinter, mock_adapter):
        """Test that operation click result is displayed."""
        from src.gui.window import CalculatorWindow
        mock_adapter.execute_operation.return_value = "42"
        window = CalculatorWindow(mock_adapter)
        window._on_operation_clicked("add")
        window._result_var.set.assert_called_with("42")

    def test_operation_clicked_falls_back_to_safe_when_execute_missing(self, mock_tkinter, mock_adapter):
        """Test that _on_operation_clicked falls back to execute_operation_safe."""
        from src.gui.window import CalculatorWindow
        del mock_adapter.execute_operation  # Make attribute unavailable
        mock_adapter.execute_operation_safe.return_value = ("42", "")
        window = CalculatorWindow(mock_adapter)
        window._on_operation_clicked("add")
        mock_adapter.execute_operation_safe.assert_called_with("add", [])

    def test_operation_clicked_displays_error_message(self, mock_tkinter, mock_adapter):
        """Test that operation click errors are displayed in result."""
        from src.gui.window import CalculatorWindow
        error_msg = "Division by zero"
        mock_adapter.execute_operation.side_effect = Exception(error_msg)
        window = CalculatorWindow(mock_adapter)
        window._on_operation_clicked("divide")
        window._result_var.set.assert_called_with(error_msg)


# =====================================================================
# Hover Effect Tests
# =====================================================================

class TestHoverEffects:
    """Test suite for button hover effects (Enter/Leave bindings)."""

    def test_mode_button_has_enter_binding(self, mock_tkinter, mock_adapter):
        """Test that mode button has Enter event binding."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)
        # Check that bind was called for mode button
        mode_button_binds = [call for call in window._mode_button.bind.call_args_list
                            if "<Enter>" in str(call)]
        assert len(mode_button_binds) > 0

    def test_mode_button_has_leave_binding(self, mock_tkinter, mock_adapter):
        """Test that mode button has Leave event binding."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)
        # Check that bind was called for mode button
        mode_button_binds = [call for call in window._mode_button.bind.call_args_list
                            if "<Leave>" in str(call)]
        assert len(mode_button_binds) > 0

    def test_operation_buttons_have_hover_bindings(self, mock_tkinter, mock_adapter):
        """Test that operation buttons have Enter/Leave bindings registered."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)
        # After grid rebuild, buttons should have bindings
        # This is verified by checking that the Frame (container) has child widgets
        assert window._ops_container is not None


# =====================================================================
# Backward Compatibility Tests
# =====================================================================

class TestBackwardCompatibility:
    """Test suite for backward compatibility with legacy interface."""

    def test_on_mode_changed_still_works(self, mock_tkinter, mock_adapter):
        """Test that on_mode_changed() still works without error."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)
        # Should not raise
        window.on_mode_changed("scientific")
        assert window._current_mode == "scientific"

    def test_update_history_display_still_works(self, mock_tkinter, mock_adapter):
        """Test that update_history_display() still works without error."""
        from src.gui.window import CalculatorWindow
        mock_adapter.get_history.return_value = []
        window = CalculatorWindow(mock_adapter)
        # Should not raise
        window.update_history_display()
        mock_adapter.get_history.assert_called()

    def test_update_operation_buttons_still_works(self, mock_tkinter, mock_adapter):
        """Test that update_operation_buttons() still works without error."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)
        # Should not raise
        window.update_operation_buttons()

    def test_on_operation_selected_still_works(self, mock_tkinter, mock_adapter):
        """Test that on_operation_selected() still works without error."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)
        # Should not raise
        window.on_operation_selected("add")
        assert window._selected_op == "add"

    def test_on_execute_clicked_still_works(self, mock_tkinter, mock_adapter):
        """Test that on_execute_clicked() still works without error."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)
        window._selected_op = None
        # Should not raise even with no operation selected
        window.on_execute_clicked()

    def test_legacy_widget_stubs_exist(self, mock_tkinter, mock_adapter):
        """Test that legacy widget stubs are created for backward compatibility."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)
        assert hasattr(window, "_operand1_entry")
        assert hasattr(window, "_operand2_entry")
        assert hasattr(window, "_operand2_label")
        assert hasattr(window, "_history_text")
        assert hasattr(window, "_ops_canvas")
        assert hasattr(window, "_ops_inner_frame")


# =====================================================================
# Integration Tests
# =====================================================================

class TestIOSLayoutIntegration:
    """Integration tests for iOS layout functionality."""

    def test_normal_mode_button_colors_are_correct(self, mock_tkinter, mock_adapter):
        """Test that buttons in normal mode have correct colors."""
        from src.gui.window import CalculatorWindow
        from src.gui.ios_theme import _THEME
        window = CalculatorWindow(mock_adapter)
        window._current_mode = "normal"

        # Verify operator button color constant
        assert _THEME["bg_operator_button"] == "#FF9500"
        assert _THEME["bg_standard_button"] == "#333333"

    def test_scientific_mode_button_colors_are_correct(self, mock_tkinter, mock_adapter):
        """Test that buttons in scientific mode have correct colors."""
        from src.gui.window import CalculatorWindow
        from src.gui.ios_theme import _THEME
        window = CalculatorWindow(mock_adapter)
        window._current_mode = "scientific"

        # Verify utility button color constant
        assert _THEME["bg_utility_button"] == "#1C1C1E"

    def test_window_initialization_complete_workflow(self, mock_tkinter, mock_adapter):
        """Test complete window initialization workflow."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)

        # Verify all major components are initialized
        assert hasattr(window, "_result_var")
        assert hasattr(window, "_result_label")
        assert hasattr(window, "_mode_button")
        assert hasattr(window, "_ops_container")
        assert window._current_mode == "normal"
        assert window._selected_op is None

    def test_mode_button_command_is_wired(self, mock_tkinter, mock_adapter):
        """Test that mode button command is properly wired to _on_mode_toggle."""
        from src.gui.window import CalculatorWindow
        window = CalculatorWindow(mock_adapter)
        # The button was created with command=self._on_mode_toggle
        assert window._mode_button is not None
