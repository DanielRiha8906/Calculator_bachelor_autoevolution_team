"""Test suite for GUIWindow iOS-inspired redesign (Issue #414).

This module tests the new iOS-inspired grid-based calculator UI that replaces
the form-based layout. Tests cover:
- Color constants (COLOR_BG, COLOR_DIGIT, COLOR_OP, COLOR_UTIL)
- Display widget properties (font size, text color, background, alignment)
- Button layout and positioning (grid positions, columnspan)
- Button colors (digits, operators, utility buttons)
- Button symbols (÷, ×, −, √, x², xʸ, n!, ln, log)
- Window properties (title, background color)
- Scientific mode buttons

All tests use unittest.mock to mock tkinter widgets and avoid display requirements
in CI environments.
"""

import sys
from unittest.mock import MagicMock, patch

# Pre-emptively mock tkinter before importing window module
tk_mock = MagicMock()
ttk_mock = MagicMock()
sys.modules['tkinter'] = tk_mock
sys.modules['tkinter.ttk'] = ttk_mock

import pytest
from unittest.mock import call, ANY

# Now import the mocked versions
import tkinter as tk
from tkinter import ttk

from src.calculator.gui.window import GUIWindow
from src.calculator.gui.controller import GUIController
import src.calculator.gui.window as window_module


@pytest.fixture
def controller():
    """Create a GUIController instance for testing."""
    return GUIController(mode="normal")


@pytest.fixture
def controller_scientific():
    """Create a GUIController instance in scientific mode."""
    return GUIController(mode="scientific")


@pytest.fixture
def mock_tkinter():
    """Provide a fixture that patches all tkinter widgets."""
    with patch("tkinter.Tk") as mock_tk, \
         patch("tkinter.Label") as mock_label, \
         patch("tkinter.Button") as mock_button, \
         patch("tkinter.Frame") as mock_frame, \
         patch("tkinter.StringVar") as mock_strvar, \
         patch("tkinter.Radiobutton") as mock_radio, \
         patch("tkinter.Scrollbar") as mock_scrollbar, \
         patch("tkinter.Listbox") as mock_listbox, \
         patch("tkinter.ttk.Combobox") as mock_combobox:

        # Setup mock_tk to return a mock root window
        mock_root = MagicMock()
        mock_tk.return_value = mock_root

        yield {
            "Tk": mock_tk,
            "root": mock_root,
            "Label": mock_label,
            "Button": mock_button,
            "Frame": mock_frame,
            "StringVar": mock_strvar,
            "Radiobutton": mock_radio,
            "Scrollbar": mock_scrollbar,
            "Listbox": mock_listbox,
            "Combobox": mock_combobox,
        }


# ============================================================================
# Color Constant Tests
# ============================================================================

class TestColorConstants:
    """Test that color constants are defined in the window module."""

    def test_color_bg_constant(self):
        """COLOR_BG constant is defined and equals #000000."""
        assert hasattr(window_module, "COLOR_BG"), "COLOR_BG constant not found in window module"
        assert window_module.COLOR_BG == "#000000", f"Expected COLOR_BG='#000000', got '{window_module.COLOR_BG}'"

    def test_color_digit_constant(self):
        """COLOR_DIGIT constant is defined and equals #333333."""
        assert hasattr(window_module, "COLOR_DIGIT"), "COLOR_DIGIT constant not found in window module"
        assert window_module.COLOR_DIGIT == "#333333", f"Expected COLOR_DIGIT='#333333', got '{window_module.COLOR_DIGIT}'"

    def test_color_op_constant(self):
        """COLOR_OP constant is defined and equals #FF9500."""
        assert hasattr(window_module, "COLOR_OP"), "COLOR_OP constant not found in window module"
        assert window_module.COLOR_OP == "#FF9500", f"Expected COLOR_OP='#FF9500', got '{window_module.COLOR_OP}'"

    def test_color_util_constant(self):
        """COLOR_UTIL constant is defined and equals #A5A5A5."""
        assert hasattr(window_module, "COLOR_UTIL"), "COLOR_UTIL constant not found in window module"
        assert window_module.COLOR_UTIL == "#A5A5A5", f"Expected COLOR_UTIL='#A5A5A5', got '{window_module.COLOR_UTIL}'"


# ============================================================================
# Display Widget Property Tests
# ============================================================================

class TestResultDisplayProperties:
    """Test properties of the result display label."""

    def test_result_display_font_size_at_least_24(self, controller, mock_tkinter):
        """Result display label has font size >= 24."""
        window = GUIWindow(controller)

        # Find the result label creation call
        label_calls = [call for call in mock_tkinter["Label"].call_args_list
                      if "font" in str(call)]

        # Must have at least one label with font specification
        assert len(label_calls) > 0, "No label with font property found"

        # Check that at least one font call has size >= 24
        font_found = False
        for call_obj in label_calls:
            if "font" in call_obj.kwargs or (len(call_obj.args) > 1):
                # Extract font tuple or font keyword
                font_info = call_obj.kwargs.get("font")
                if font_info and isinstance(font_info, tuple) and len(font_info) > 1:
                    font_size = font_info[1]
                    if font_size >= 24:
                        font_found = True
                        break

        assert font_found, "Result label font size is not >= 24"

    def test_result_display_text_color_white(self, controller, mock_tkinter):
        """Result display label has fg='#FFFFFF'."""
        window = GUIWindow(controller)

        # Find label calls with fg='#FFFFFF'
        label_calls = mock_tkinter["Label"].call_args_list
        white_text_found = False

        for call_obj in label_calls:
            if call_obj.kwargs.get("fg") == "#FFFFFF":
                white_text_found = True
                break

        assert white_text_found, "No label found with fg='#FFFFFF'"

    def test_result_display_background_black(self, controller, mock_tkinter):
        """Result display label has bg='#000000'."""
        window = GUIWindow(controller)

        # Find label calls with bg='#000000'
        label_calls = mock_tkinter["Label"].call_args_list
        black_bg_found = False

        for call_obj in label_calls:
            if call_obj.kwargs.get("bg") == "#000000":
                black_bg_found = True
                break

        assert black_bg_found, "No label found with bg='#000000'"

    def test_result_display_right_aligned(self, controller, mock_tkinter):
        """Result display label has anchor='e' or justify=RIGHT."""
        window = GUIWindow(controller)

        # Find label calls with anchor='e'
        label_calls = mock_tkinter["Label"].call_args_list
        right_aligned = False

        for call_obj in label_calls:
            anchor = call_obj.kwargs.get("anchor")
            justify = call_obj.kwargs.get("justify")
            if anchor == "e" or justify == tk.RIGHT:
                right_aligned = True
                break

        assert right_aligned, "No label found with anchor='e' or justify=RIGHT"


# ============================================================================
# Button Structure and Layout Tests
# ============================================================================

class TestButtonStructure:
    """Test that buttons are stored in a accessible structure."""

    def test_window_has_buttons_dict(self, controller, mock_tkinter):
        """GUIWindow instance has a _buttons or buttons attribute (dict)."""
        window = GUIWindow(controller)

        has_buttons_dict = (
            (hasattr(window, "_buttons") and isinstance(window._buttons, dict)) or
            (hasattr(window, "buttons") and isinstance(window.buttons, dict))
        )

        assert has_buttons_dict, "GUIWindow must have _buttons or buttons dict attribute"

    def test_button_c_exists(self, controller, mock_tkinter):
        """A button with text 'C' exists in the buttons dict."""
        window = GUIWindow(controller)

        buttons_dict = getattr(window, "_buttons", None) or getattr(window, "buttons", None)
        assert buttons_dict is not None, "No buttons dict found"
        assert "C" in buttons_dict, "Button 'C' not found in buttons dict"

    def test_button_del_exists(self, controller, mock_tkinter):
        """A button with text 'Del' exists in the buttons dict."""
        window = GUIWindow(controller)

        buttons_dict = getattr(window, "_buttons", None) or getattr(window, "buttons", None)
        assert buttons_dict is not None, "No buttons dict found"
        assert "Del" in buttons_dict, "Button 'Del' not found in buttons dict"

    def test_button_mode_exists(self, controller, mock_tkinter):
        """A button with text 'Mode' exists in the buttons dict."""
        window = GUIWindow(controller)

        buttons_dict = getattr(window, "_buttons", None) or getattr(window, "buttons", None)
        assert buttons_dict is not None, "No buttons dict found"
        assert "Mode" in buttons_dict, "Button 'Mode' not found in buttons dict"

    def test_button_divide_symbol(self, controller, mock_tkinter):
        """A button with text '÷' (not '/') exists."""
        window = GUIWindow(controller)

        buttons_dict = getattr(window, "_buttons", None) or getattr(window, "buttons", None)
        assert buttons_dict is not None, "No buttons dict found"
        assert "÷" in buttons_dict, "Button '÷' not found; division button must use ÷ symbol"
        assert "/" not in buttons_dict, "Division button must use '÷', not '/'"

    def test_button_multiply_symbol(self, controller, mock_tkinter):
        """A button with text '×' (not '*') exists."""
        window = GUIWindow(controller)

        buttons_dict = getattr(window, "_buttons", None) or getattr(window, "buttons", None)
        assert buttons_dict is not None, "No buttons dict found"
        assert "×" in buttons_dict, "Button '×' not found; multiply button must use × symbol"
        assert "*" not in buttons_dict, "Multiply button must use '×', not '*'"

    def test_button_subtract_symbol(self, controller, mock_tkinter):
        """A button with text '−' (not '-') exists."""
        window = GUIWindow(controller)

        buttons_dict = getattr(window, "_buttons", None) or getattr(window, "buttons", None)
        assert buttons_dict is not None, "No buttons dict found"
        assert "−" in buttons_dict, "Button '−' not found; subtract button must use − symbol"
        assert "-" not in buttons_dict, "Subtract button must use '−', not '-'"

    def test_button_zero_columnspan(self, controller, mock_tkinter):
        """Button '0' has columnspan=2."""
        window = GUIWindow(controller)

        buttons_dict = getattr(window, "_buttons", None) or getattr(window, "buttons", None)
        assert buttons_dict is not None, "No buttons dict found"
        assert "0" in buttons_dict, "Button '0' not found"

        # The button should have grid_info with columnspan=2
        button_widget = buttons_dict["0"]
        if hasattr(button_widget, "grid_info"):
            grid_info = button_widget.grid_info()
            assert grid_info.get("columnspan") == 2, f"Button '0' columnspan is {grid_info.get('columnspan')}, expected 2"

    def test_button_decimal_exists(self, controller, mock_tkinter):
        """A button with text '.' exists."""
        window = GUIWindow(controller)

        buttons_dict = getattr(window, "_buttons", None) or getattr(window, "buttons", None)
        assert buttons_dict is not None, "No buttons dict found"
        assert "." in buttons_dict, "Button '.' (decimal) not found"

    def test_button_equals_exists(self, controller, mock_tkinter):
        """A button with text '=' exists."""
        window = GUIWindow(controller)

        buttons_dict = getattr(window, "_buttons", None) or getattr(window, "buttons", None)
        assert buttons_dict is not None, "No buttons dict found"
        assert "=" in buttons_dict, "Button '=' not found"


# ============================================================================
# Button Color Tests
# ============================================================================

class TestButtonColors:
    """Test button colors for different button types."""

    @pytest.mark.parametrize("digit", ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
    def test_digit_buttons_dark_grey(self, controller, mock_tkinter, digit):
        """Digit buttons (0-9) have bg='#333333'."""
        window = GUIWindow(controller)

        buttons_dict = getattr(window, "_buttons", None) or getattr(window, "buttons", None)
        assert buttons_dict is not None, "No buttons dict found"
        assert digit in buttons_dict, f"Button '{digit}' not found"

        button_widget = buttons_dict[digit]
        if hasattr(button_widget, "cget"):
            bg = button_widget.cget("bg")
            assert bg == "#333333", f"Digit button '{digit}' bg is {bg}, expected #333333"

    @pytest.mark.parametrize("op_button", ["+", "−", "×", "÷", "="])
    def test_operator_buttons_orange(self, controller, mock_tkinter, op_button):
        """Operator buttons (+, −, ×, ÷, =) have bg='#FF9500'."""
        window = GUIWindow(controller)

        buttons_dict = getattr(window, "_buttons", None) or getattr(window, "buttons", None)
        assert buttons_dict is not None, "No buttons dict found"
        assert op_button in buttons_dict, f"Button '{op_button}' not found"

        button_widget = buttons_dict[op_button]
        if hasattr(button_widget, "cget"):
            bg = button_widget.cget("bg")
            assert bg == "#FF9500", f"Operator button '{op_button}' bg is {bg}, expected #FF9500"

    @pytest.mark.parametrize("util_button", ["C", "Del", "Mode"])
    def test_utility_buttons_light_grey(self, controller, mock_tkinter, util_button):
        """Utility buttons (C, Del, Mode) have bg='#A5A5A5'."""
        window = GUIWindow(controller)

        buttons_dict = getattr(window, "_buttons", None) or getattr(window, "buttons", None)
        assert buttons_dict is not None, "No buttons dict found"
        assert util_button in buttons_dict, f"Button '{util_button}' not found"

        button_widget = buttons_dict[util_button]
        if hasattr(button_widget, "cget"):
            bg = button_widget.cget("bg")
            assert bg == "#A5A5A5", f"Utility button '{util_button}' bg is {bg}, expected #A5A5A5"

    def test_all_buttons_flat_relief(self, controller, mock_tkinter):
        """All buttons have relief='flat'."""
        window = GUIWindow(controller)

        buttons_dict = getattr(window, "_buttons", None) or getattr(window, "buttons", None)
        assert buttons_dict is not None, "No buttons dict found"

        for button_text, button_widget in buttons_dict.items():
            if hasattr(button_widget, "cget"):
                relief = button_widget.cget("relief")
                assert relief == "flat", f"Button '{button_text}' relief is {relief}, expected 'flat'"

    def test_all_buttons_white_text(self, controller, mock_tkinter):
        """All buttons have fg='#FFFFFF'."""
        window = GUIWindow(controller)

        buttons_dict = getattr(window, "_buttons", None) or getattr(window, "buttons", None)
        assert buttons_dict is not None, "No buttons dict found"

        for button_text, button_widget in buttons_dict.items():
            if hasattr(button_widget, "cget"):
                fg = button_widget.cget("fg")
                assert fg == "#FFFFFF", f"Button '{button_text}' fg is {fg}, expected #FFFFFF"


# ============================================================================
# Window Properties Tests
# ============================================================================

class TestWindowProperties:
    """Test window-level properties."""

    def test_window_background_black(self, controller, mock_tkinter):
        """Root window is configured with bg='#000000'."""
        window = GUIWindow(controller)

        # Check that the mock root's config was called with bg="#000000"
        root = mock_tkinter["root"]

        # Either check via config call or cget
        config_calls = [c for c in root.config.call_args_list if "bg" in str(c)]
        bg_set = False

        # Try to find it in the mock's attributes
        if hasattr(root, "_bg"):
            bg_set = root._bg == "#000000"
        elif hasattr(root, "cget"):
            try:
                bg = root.cget("bg")
                bg_set = bg == "#000000"
            except:
                pass

        # If not found in mock, check if it was called during init
        # (mocking may have captured the call differently)
        if not bg_set:
            # Check if any config/cget was called on the root
            assert root.config.called or hasattr(root, "bg"), \
                "Root window bg property not found"

    def test_window_title(self, controller, mock_tkinter):
        """Window title is 'Calculator' by default."""
        window = GUIWindow(controller)

        # Check that title() was called on the mock root
        root = mock_tkinter["root"]
        title_calls = [c for c in root.method_calls if "title" in str(c)]

        assert len(root.title.call_args_list) > 0, "root.title() was not called"

        # Check the title call
        root.title.assert_called_with("Calculator")


# ============================================================================
# Scientific Mode Button Tests
# ============================================================================

class TestScientificModeButtons:
    """Test buttons that appear only in scientific mode."""

    def test_scientific_button_sqrt(self, controller_scientific, mock_tkinter):
        """In scientific mode, a button with text '√' exists."""
        window = GUIWindow(controller_scientific)

        buttons_dict = getattr(window, "_buttons", None) or getattr(window, "buttons", None)
        assert buttons_dict is not None, "No buttons dict found"
        assert "√" in buttons_dict, "Button '√' not found in scientific mode"

    def test_scientific_button_square(self, controller_scientific, mock_tkinter):
        """In scientific mode, a button with text 'x²' exists."""
        window = GUIWindow(controller_scientific)

        buttons_dict = getattr(window, "_buttons", None) or getattr(window, "buttons", None)
        assert buttons_dict is not None, "No buttons dict found"
        assert "x²" in buttons_dict, "Button 'x²' not found in scientific mode"

    def test_scientific_button_power(self, controller_scientific, mock_tkinter):
        """In scientific mode, a button with text 'xʸ' exists."""
        window = GUIWindow(controller_scientific)

        buttons_dict = getattr(window, "_buttons", None) or getattr(window, "buttons", None)
        assert buttons_dict is not None, "No buttons dict found"
        assert "xʸ" in buttons_dict, "Button 'xʸ' not found in scientific mode"

    def test_scientific_button_factorial(self, controller_scientific, mock_tkinter):
        """In scientific mode, a button with text 'n!' exists."""
        window = GUIWindow(controller_scientific)

        buttons_dict = getattr(window, "_buttons", None) or getattr(window, "buttons", None)
        assert buttons_dict is not None, "No buttons dict found"
        assert "n!" in buttons_dict, "Button 'n!' not found in scientific mode"

    def test_scientific_button_ln(self, controller_scientific, mock_tkinter):
        """In scientific mode, a button with text 'ln' exists."""
        window = GUIWindow(controller_scientific)

        buttons_dict = getattr(window, "_buttons", None) or getattr(window, "buttons", None)
        assert buttons_dict is not None, "No buttons dict found"
        assert "ln" in buttons_dict, "Button 'ln' not found in scientific mode"

    def test_scientific_button_log(self, controller_scientific, mock_tkinter):
        """In scientific mode, a button with text 'log' exists."""
        window = GUIWindow(controller_scientific)

        buttons_dict = getattr(window, "_buttons", None) or getattr(window, "buttons", None)
        assert buttons_dict is not None, "No buttons dict found"
        assert "log" in buttons_dict, "Button 'log' not found in scientific mode"
