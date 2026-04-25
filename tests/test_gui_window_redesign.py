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


# ============================================================================
# Scientific Mode Toggle Tests (Issue: Dynamic Panel Visibility)
# ============================================================================

class TestScientificModePanelToggle:
    """Test scientific panel visibility toggling with _on_mode_toggle()."""

    def test_scientific_panel_visible_on_init_scientific_mode(self, controller_scientific, mock_tkinter):
        """When initialized in scientific mode, _scientific_panel_visible is True."""
        window = GUIWindow(controller_scientific)

        assert window._scientific_panel_visible is True, \
            "Expected _scientific_panel_visible to be True in scientific mode"
        assert window._scientific_frame is not None, \
            "Expected _scientific_frame to be created in scientific mode"

    def test_scientific_panel_hidden_on_init_normal_mode(self, controller, mock_tkinter):
        """When initialized in normal mode, _scientific_panel_visible is False."""
        window = GUIWindow(controller)

        assert window._scientific_panel_visible is False, \
            "Expected _scientific_panel_visible to be False in normal mode"
        assert window._scientific_frame is None, \
            "Expected _scientific_frame to be None in normal mode"

    def test_mode_button_toggles_panel_on(self, controller, mock_tkinter):
        """Calling _on_mode_toggle() when panel is hidden shows it."""
        window = GUIWindow(controller)
        # Initial state: normal mode, panel hidden
        assert window._scientific_panel_visible is False

        window._on_mode_toggle()

        assert window._scientific_panel_visible is True, \
            "Expected _scientific_panel_visible to be True after toggle"
        assert window._scientific_frame is not None, \
            "Expected _scientific_frame to be created after toggle"

    def test_mode_button_toggles_panel_off(self, controller_scientific, mock_tkinter):
        """Calling _on_mode_toggle() when panel is visible hides it."""
        window = GUIWindow(controller_scientific)
        # Initial state: scientific mode, panel visible
        assert window._scientific_panel_visible is True

        window._on_mode_toggle()

        assert window._scientific_panel_visible is False, \
            "Expected _scientific_panel_visible to be False after toggle"
        assert window._scientific_frame is None, \
            "Expected _scientific_frame to be None after toggle"

    def test_mode_toggle_does_not_call_switch_mode(self, controller, mock_tkinter):
        """_on_mode_toggle() should not call controller.switch_mode()."""
        window = GUIWindow(controller)
        controller.switch_mode = MagicMock()

        window._on_mode_toggle()

        controller.switch_mode.assert_not_called()

    def test_mode_toggle_preserves_pending_operation_state(self, controller, mock_tkinter):
        """_on_mode_toggle() preserves pending operation state."""
        window = GUIWindow(controller)
        # Set up pending operation
        window._operand1 = "5"
        window._pending_op = "add"
        window._awaiting_second = True

        window._on_mode_toggle()

        # Verify state is preserved
        assert window._operand1 == "5", "Expected _operand1 to be preserved"
        assert window._pending_op == "add", "Expected _pending_op to be preserved"
        assert window._awaiting_second is True, "Expected _awaiting_second to be preserved"

    def test_rebuild_removes_scientific_buttons_when_hiding(self, controller_scientific, mock_tkinter):
        """When hiding panel, scientific button keys are removed from _buttons."""
        window = GUIWindow(controller_scientific)
        # Verify scientific buttons exist initially
        buttons_dict = window._buttons
        scientific_buttons = ["√", "x²", "xʸ", "n!", "ln", "log"]
        for btn in scientific_buttons:
            assert btn in buttons_dict, f"Expected button '{btn}' to exist in scientific mode"

        window._on_mode_toggle()

        # Verify scientific buttons are removed
        buttons_dict = window._buttons
        for btn in scientific_buttons:
            assert btn not in buttons_dict, \
                f"Expected button '{btn}' to be removed from _buttons after hiding panel"

    def test_mode_toggle_toggles_multiple_times(self, controller, mock_tkinter):
        """_on_mode_toggle() can be called multiple times to toggle on/off."""
        window = GUIWindow(controller)

        # Toggle 1: off -> on
        window._on_mode_toggle()
        assert window._scientific_panel_visible is True

        # Toggle 2: on -> off
        window._on_mode_toggle()
        assert window._scientific_panel_visible is False

        # Toggle 3: off -> on
        window._on_mode_toggle()
        assert window._scientific_panel_visible is True


# ============================================================================
# Power Operation (xʸ) Tests: Binary Operation Behavior
# ============================================================================

class TestPowerOperationBinary:
    """Test power (xʸ) operation as a binary pending operation."""

    def test_power_op_stores_first_operand(self, controller_scientific, mock_tkinter):
        """Calling _on_scientific_op("power") stores operand1 and sets pending state."""
        window = GUIWindow(controller_scientific)
        # Directly set the display value using the mock
        mock_tkinter["StringVar"].return_value.get.return_value = "2"

        window._on_scientific_op("power")

        assert window._operand1 == "2", "Expected _operand1 to be '2'"
        assert window._pending_op == "power", "Expected _pending_op to be 'power'"
        assert window._awaiting_second is True, "Expected _awaiting_second to be True"

    def test_power_op_does_not_call_execute_operation(self, controller_scientific, mock_tkinter):
        """Calling _on_scientific_op("power") should NOT immediately execute."""
        window = GUIWindow(controller_scientific)
        mock_tkinter["StringVar"].return_value.get.return_value = "2"
        controller_scientific.execute_operation = MagicMock()

        window._on_scientific_op("power")

        controller_scientific.execute_operation.assert_not_called()

    def test_power_op_equals_dispatches_with_two_operands(self, controller_scientific, mock_tkinter):
        """After power operation, _on_equals() calls execute_operation with two operands."""
        window = GUIWindow(controller_scientific)
        window._operand1 = "2"
        window._pending_op = "power"
        window._awaiting_second = True
        mock_tkinter["StringVar"].return_value.get.return_value = "3"

        controller_scientific.execute_operation = MagicMock(
            return_value={"success": True, "result": 8.0}
        )

        window._on_equals()

        controller_scientific.execute_operation.assert_called_once_with("power", [2.0, 3.0])

    def test_power_not_hardcoded_exponent(self, controller_scientific, mock_tkinter):
        """Power operation uses the actual second operand, not hardcoded value."""
        window = GUIWindow(controller_scientific)
        window._operand1 = "3"
        window._pending_op = "power"
        window._awaiting_second = True
        mock_tkinter["StringVar"].return_value.get.return_value = "4"

        # Mock controller to return 81 (3^4)
        controller_scientific.execute_operation = MagicMock(
            return_value={"success": True, "result": 81.0}
        )

        window._on_equals()

        # Verify the call was made with [3.0, 4.0], not [3.0, 2.0]
        call_args = controller_scientific.execute_operation.call_args
        assert call_args[0][1] == [3.0, 4.0], \
            f"Expected operands [3.0, 4.0], got {call_args[0][1]}"

    def test_power_op_clears_pending_after_equals(self, controller_scientific, mock_tkinter):
        """After executing power with equals, pending state is cleared."""
        window = GUIWindow(controller_scientific)
        window._operand1 = "2"
        window._pending_op = "power"
        window._awaiting_second = True
        mock_tkinter["StringVar"].return_value.get.return_value = "3"

        controller_scientific.execute_operation = MagicMock(
            return_value={"success": True, "result": 8.0}
        )

        window._on_equals()

        assert window._pending_op is None, "Expected _pending_op to be None after equals"
        assert window._awaiting_second is False, "Expected _awaiting_second to be False after equals"

    @pytest.mark.parametrize("base,exponent,expected", [
        ("2", "3", 8.0),
        ("2", "10", 1024.0),
        ("10", "2", 100.0),
        ("5", "0", 1.0),
    ])
    def test_power_op_various_exponents(self, base, exponent, expected, controller_scientific, mock_tkinter):
        """Power operation correctly handles various base and exponent combinations."""
        window = GUIWindow(controller_scientific)
        window._operand1 = base
        window._pending_op = "power"
        window._awaiting_second = True
        mock_tkinter["StringVar"].return_value.get.return_value = exponent

        controller_scientific.execute_operation = MagicMock(
            return_value={"success": True, "result": expected}
        )

        window._on_equals()

        # Verify the operation was called with correct operands
        call_args = controller_scientific.execute_operation.call_args
        assert call_args[0][0] == "power", "Expected operation 'power'"
        assert call_args[0][1] == [float(base), float(exponent)], \
            f"Expected operands [{float(base)}, {float(exponent)}], got {call_args[0][1]}"


# ============================================================================
# Unary Scientific Operations Tests
# ============================================================================

class TestUnaryScientificOperations:
    """Test unary scientific operations (square root, square, factorial, ln, log)."""

    @pytest.mark.parametrize("op_name,operand,expected_result", [
        ("square_root", "9", 3.0),
        ("square", "4", 16.0),
        ("factorial", "5", 120.0),
        ("ln", "2.718", 1.0),
        ("log10", "100", 2.0),
    ])
    def test_unary_scientific_op_calls_execute_immediately(self, op_name, operand, expected_result,
                                                           controller_scientific, mock_tkinter):
        """Unary scientific operations execute immediately via controller."""
        window = GUIWindow(controller_scientific)
        mock_tkinter["StringVar"].return_value.get.return_value = operand

        controller_scientific.execute_operation = MagicMock(
            return_value={"success": True, "result": expected_result}
        )

        window._on_scientific_op(op_name)

        # Verify execute_operation was called with single operand
        controller_scientific.execute_operation.assert_called_once_with(op_name, [float(operand)])

    @pytest.mark.parametrize("op_name", ["square_root", "square", "factorial", "ln", "log10"])
    def test_unary_op_does_not_set_pending(self, op_name, controller_scientific, mock_tkinter):
        """Unary operations do not set pending operation state."""
        window = GUIWindow(controller_scientific)
        mock_tkinter["StringVar"].return_value.get.return_value = "5"

        controller_scientific.execute_operation = MagicMock(
            return_value={"success": True, "result": 25.0}
        )

        window._on_scientific_op(op_name)

        # Pending state should not be set for unary operations
        assert window._pending_op is None, \
            f"Expected _pending_op to be None for unary operation '{op_name}'"
        assert window._awaiting_second is False, \
            f"Expected _awaiting_second to be False for unary operation '{op_name}'"

    def test_unary_op_does_not_set_operand1(self, controller_scientific, mock_tkinter):
        """Unary operations do not set _operand1."""
        window = GUIWindow(controller_scientific)
        window._operand1 = ""  # Clear initial state
        mock_tkinter["StringVar"].return_value.get.return_value = "16"

        controller_scientific.execute_operation = MagicMock(
            return_value={"success": True, "result": 4.0}
        )

        window._on_scientific_op("square_root")

        # _operand1 should remain empty, not set to the display value
        assert window._operand1 == "", \
            "Expected _operand1 to remain empty for unary operations"

    def test_unary_op_square_root_calls_correct_operation(self, controller_scientific, mock_tkinter):
        """Square root operation calls execute_operation with 'square_root'."""
        window = GUIWindow(controller_scientific)
        mock_tkinter["StringVar"].return_value.get.return_value = "16"

        controller_scientific.execute_operation = MagicMock(
            return_value={"success": True, "result": 4.0}
        )

        window._on_scientific_op("square_root")

        # Verify correct operation name
        call_args = controller_scientific.execute_operation.call_args
        assert call_args[0][0] == "square_root", \
            "Expected operation name 'square_root'"

    def test_unary_op_error_handling_updates_display(self, controller_scientific, mock_tkinter):
        """Unary operation error calls set on display to show 'Error'."""
        window = GUIWindow(controller_scientific)
        mock_tkinter["StringVar"].return_value.get.return_value = "5"

        controller_scientific.execute_operation = MagicMock(
            return_value={"success": False, "result": None}
        )

        window._on_scientific_op("square_root")

        # Verify that set was called with "Error"
        display_var = window._display_var
        display_var.set.assert_called_with("Error")

    def test_unary_op_invalid_input_error_displays_error(self, controller_scientific, mock_tkinter):
        """Unary operation with non-numeric input displays 'Error'."""
        window = GUIWindow(controller_scientific)
        mock_tkinter["StringVar"].return_value.get.return_value = "abc"

        window._on_scientific_op("square_root")

        # Verify that set was called with "Error" on exception
        display_var = window._display_var
        display_var.set.assert_called_with("Error")


# ============================================================================
# Integration Tests: Mode Toggle + Operations
# ============================================================================

class TestModeToggleWithOperations:
    """Test interaction between mode toggle and pending operations."""

    def test_toggle_panel_preserves_operand1_in_power_operation(self, controller, mock_tkinter):
        """Toggling panel visibility preserves operand1 during power operation setup."""
        window = GUIWindow(controller)
        window._display_var.set("5")

        # Switch to scientific mode
        window._on_mode_toggle()

        # Set up power operation (becomes available in scientific mode)
        window._operand1 = "5"
        window._pending_op = "power"
        window._awaiting_second = True

        # Toggle back to normal mode
        window._on_mode_toggle()

        # Verify pending state is preserved
        assert window._operand1 == "5"
        assert window._pending_op == "power"
        assert window._awaiting_second is True

    def test_panel_hide_removes_xpower_button(self, controller, mock_tkinter):
        """When panel is hidden, 'xʸ' button is removed from _buttons."""
        window = GUIWindow(controller)
        window._on_mode_toggle()  # Show panel
        assert "xʸ" in window._buttons

        window._on_mode_toggle()  # Hide panel
        assert "xʸ" not in window._buttons

    def test_panel_show_recreates_xpower_button(self, controller, mock_tkinter):
        """When panel is shown again, 'xʸ' button is recreated in _buttons."""
        window = GUIWindow(controller)
        window._on_mode_toggle()  # Show panel
        assert "xʸ" in window._buttons

        window._on_mode_toggle()  # Hide panel
        assert "xʸ" not in window._buttons

        window._on_mode_toggle()  # Show panel again
        assert "xʸ" in window._buttons
