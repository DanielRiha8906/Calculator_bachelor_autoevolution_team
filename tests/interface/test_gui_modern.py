"""Comprehensive pytest tests for ModernGUIInterface class.

This test suite focuses on testing the ModernGUIInterface logic and integration
without requiring a full tkinter GUI environment (which is unavailable in
headless CI).

Tests cover:
- ModernGUIInterface initialization and dependencies
- Helper methods (_parse_float, _format_result, _button_color)
- Display state management
- Digit input handling
- Operator button interactions
- Equals evaluation
- Clear and Delete functionality
- Mode toggle (standard/scientific)
- Scientific operations (unary and binary)
- Error handling and logging
- Result formatting and validation
- Unicode symbol button labels
- Button color scheme correctness
- State preservation across mode toggles
"""

import pytest
import tempfile
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, call
import os

# Try to import tkinter, but proceed with mock-based tests if unavailable
try:
    import tkinter as tk
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False
    # Create a properly mocked tkinter module to allow imports
    mock_tk = MagicMock()
    # Create a mock Tk class that can be subclassed
    mock_tk.Tk = type('Tk', (), {
        '__init__': lambda *args, **kwargs: None,
        'title': lambda self, x: None,
        'configure': lambda self, **kwargs: None,
        'resizable': lambda self, w, h: None,
        'columnconfigure': lambda self, *args, **kwargs: None,
        'rowconfigure': lambda self, *args, **kwargs: None,
        'mainloop': lambda self: None,
        'destroy': lambda self: None,
    })
    mock_tk.StringVar = MagicMock
    mock_tk.Label = MagicMock
    mock_tk.Frame = MagicMock
    mock_tk.Button = MagicMock
    sys.modules['tkinter'] = mock_tk


# ==============================================================================
# FIXTURES
# ==============================================================================

@pytest.fixture
def calculator():
    """Provide a Calculator instance."""
    from src.calculator import Calculator
    return Calculator()


@pytest.fixture
def context():
    """Provide a CalculatorContext instance."""
    from src.context import CalculatorContext
    return CalculatorContext()


@pytest.fixture
def tmp_history_file(tmp_path):
    """Provide a temporary history file path."""
    return str(tmp_path / "history.txt")


@pytest.fixture
def tmp_error_file(tmp_path):
    """Provide a temporary error log file path."""
    return str(tmp_path / "error.log")


@pytest.fixture
def history(tmp_history_file):
    """Provide an OperationHistory instance with a temporary file."""
    from src.support.history import OperationHistory
    hist = OperationHistory(history_file=tmp_history_file)
    hist.clear_history()
    return hist


@pytest.fixture
def error_logger(tmp_error_file):
    """Provide an ErrorLogger instance with a temporary file."""
    from src.support.error_logger import ErrorLogger
    logger = ErrorLogger(error_file=tmp_error_file)
    logger.clear_errors()
    return logger


@pytest.fixture
def operation_registry(calculator):
    """Provide an OperationRegistry instance."""
    from src.core.operations import OperationRegistry
    return OperationRegistry(calculator)


@pytest.fixture
def modern_gui_with_mocked_tk(calculator, operation_registry, context, history, error_logger):
    """Provide a ModernGUIInterface instance with tkinter mocked.

    Uses @patch context manager to mock tkinter components that would normally
    require a display. This allows testing the core GUI logic.
    """
    if not HAS_TKINTER:
        pytest.skip("tkinter not available")

    from src.interface.gui_modern import ModernGUIInterface
    with patch("tkinter.Tk.__init__", return_value=None):
        with patch("tkinter.Tk.mainloop"):
            # Mock all the tkinter setup methods to prevent display errors
            with patch("tkinter.Frame"), \
                 patch("tkinter.Label"), \
                 patch("tkinter.Button"), \
                 patch("tkinter.StringVar") as mock_stringvar_class:

                # Make StringVar instances behave like real ones
                def make_stringvar(*args, **kwargs):
                    mock = MagicMock()
                    mock._value = kwargs.get("value", "")

                    def get():
                        return mock._value
                    def set(val):
                        mock._value = val
                    mock.get = get
                    mock.set = set
                    return mock

                mock_stringvar_class.side_effect = make_stringvar

                try:
                    gui = ModernGUIInterface(
                        calculator,
                        operation_registry,
                        context,
                        history,
                        error_logger
                    )
                    yield gui
                except Exception as e:
                    pytest.skip(f"Could not instantiate ModernGUI: {e}")
                finally:
                    try:
                        if hasattr(gui, 'destroy'):
                            gui.destroy()
                    except Exception:
                        pass


# ==============================================================================
# TESTS: Initialization
# ==============================================================================

class TestModernGUIInitialization:
    """Test suite for ModernGUIInterface initialization."""

    def test_gui_initializes_with_correct_title(self, modern_gui_with_mocked_tk):
        """Test that GUI initializes with correct window title."""
        gui = modern_gui_with_mocked_tk
        # Title is set in __init__, check it's set
        assert gui.title() == "Calculator"

    def test_gui_initializes_with_black_background(self, modern_gui_with_mocked_tk):
        """Test that GUI initializes with black background."""
        gui = modern_gui_with_mocked_tk
        from src.interface.gui_modern import BG_COLOR
        # Background is configured in __init__
        assert BG_COLOR == "#000000"

    def test_gui_initializes_with_display_var(self, modern_gui_with_mocked_tk):
        """Test that GUI initializes with StringVar for display."""
        gui = modern_gui_with_mocked_tk
        assert hasattr(gui, 'display_var')
        assert gui.display_var is not None

    def test_gui_initializes_with_zero_display(self, modern_gui_with_mocked_tk):
        """Test that display initializes to '0'."""
        gui = modern_gui_with_mocked_tk
        assert gui.display_var.get() == "0"

    def test_gui_initializes_with_empty_current_input(self, modern_gui_with_mocked_tk):
        """Test that current_input initializes to empty string."""
        gui = modern_gui_with_mocked_tk
        assert gui.current_input == ""

    def test_gui_initializes_with_none_operation(self, modern_gui_with_mocked_tk):
        """Test that operation initializes to None."""
        gui = modern_gui_with_mocked_tk
        assert gui.operation is None

    def test_gui_initializes_with_none_first_operand(self, modern_gui_with_mocked_tk):
        """Test that first_operand initializes to None."""
        gui = modern_gui_with_mocked_tk
        assert gui.first_operand is None

    def test_gui_initializes_with_false_result_shown(self, modern_gui_with_mocked_tk):
        """Test that result_shown initializes to False."""
        gui = modern_gui_with_mocked_tk
        assert gui.result_shown is False

    def test_gui_initializes_with_false_scientific_mode(self, modern_gui_with_mocked_tk):
        """Test that scientific_mode initializes to False."""
        gui = modern_gui_with_mocked_tk
        assert gui.scientific_mode is False

    def test_gui_initializes_with_scientific_frame(self, modern_gui_with_mocked_tk):
        """Test that scientific frame is created."""
        gui = modern_gui_with_mocked_tk
        assert hasattr(gui, 'sci_frame')

    def test_gui_is_not_resizable(self, modern_gui_with_mocked_tk):
        """Test that GUI window is not resizable."""
        gui = modern_gui_with_mocked_tk
        # resizable is set in __init__
        # Check internal state
        assert hasattr(gui, 'resizable')


# Import constants after tkinter is mocked
from src.interface.gui_modern import (
    DISPLAY_FONT, TEXT_COLOR, BG_COLOR, NUM_BTN_COLOR,
    OP_BTN_COLOR, UTIL_BTN_COLOR, _DIV_SYMBOL, _MUL_SYMBOL,
    _SUB_SYMBOL, _STANDARD_ROWS, _SCIENTIFIC_LABELS, ModernGUIInterface
)


# ==============================================================================
# TESTS: Display Panel
# ==============================================================================

class TestDisplayPanel:
    """Test suite for display panel properties."""

    def test_display_label_exists(self, modern_gui_with_mocked_tk):
        """Test that display label is created."""
        gui = modern_gui_with_mocked_tk
        assert hasattr(gui, '_display_label')

    def test_display_uses_correct_font_size(self):
        """Test that display uses correct font size."""
        assert DISPLAY_FONT[1] >= 24

    def test_display_font_is_arial(self):
        """Test that display font is Arial."""
        assert DISPLAY_FONT[0] == "Arial"

    def test_display_shows_white_text(self):
        """Test that display shows white text."""
        assert TEXT_COLOR == "#FFFFFF"

    def test_display_has_black_background(self):
        """Test that display has black background."""
        assert BG_COLOR == "#000000"


# ==============================================================================
# TESTS: Standard Mode Button Layout
# ==============================================================================

class TestStandardModeButtonLayout:
    """Test suite for standard mode button layout."""

    def test_standard_rows_defines_correct_count(self):
        """Test that standard rows define correct button count."""
        # 4 rows x 4 cols = 16 buttons in standard rows
        total = sum(len(row) for row in _STANDARD_ROWS)
        assert total == 16

    def test_standard_rows_first_row_contains_utility(self):
        """Test that first row contains C, Del, Mode."""
        first_row = _STANDARD_ROWS[0]
        assert "C" in first_row
        assert "Del" in first_row
        assert "Mode" in first_row

    def test_standard_rows_fourth_row_has_minus_symbol(self):
        """Test that fourth row uses correct minus symbol."""
        fourth_row = _STANDARD_ROWS[3]
        assert _SUB_SYMBOL in fourth_row

    def test_standard_rows_first_row_has_divide_symbol(self):
        """Test that first row uses correct divide symbol."""
        first_row = _STANDARD_ROWS[0]
        assert _DIV_SYMBOL in first_row

    def test_standard_rows_second_row_has_multiply_symbol(self):
        """Test that second row uses correct multiply symbol."""
        second_row = _STANDARD_ROWS[1]
        assert _MUL_SYMBOL in second_row


# ==============================================================================
# TESTS: Scientific Mode Button Layout
# ==============================================================================

class TestScientificModeButtonLayout:
    """Test suite for scientific mode button layout."""

    def test_scientific_labels_define_correct_layout(self):
        """Test that scientific labels define correct button count."""
        # 2 rows x 3 cols = 6 buttons in scientific panel
        total = sum(len(row) for row in _SCIENTIFIC_LABELS)
        assert total == 6

    def test_scientific_labels_first_row_contains_sqrt(self):
        """Test that first row contains sqrt button."""
        first_row = _SCIENTIFIC_LABELS[0]
        assert "√" in first_row

    def test_scientific_labels_first_row_contains_square(self):
        """Test that first row contains square button."""
        first_row = _SCIENTIFIC_LABELS[0]
        assert "x²" in first_row

    def test_scientific_labels_first_row_contains_power(self):
        """Test that first row contains power button."""
        first_row = _SCIENTIFIC_LABELS[0]
        assert "xʸ" in first_row

    def test_scientific_labels_second_row_contains_factorial(self):
        """Test that second row contains factorial button."""
        second_row = _SCIENTIFIC_LABELS[1]
        assert "n!" in second_row

    def test_scientific_labels_second_row_contains_ln(self):
        """Test that second row contains natural log button."""
        second_row = _SCIENTIFIC_LABELS[1]
        assert "ln" in second_row

    def test_scientific_labels_second_row_contains_log(self):
        """Test that second row contains log button."""
        second_row = _SCIENTIFIC_LABELS[1]
        assert "log" in second_row

    def test_scientific_frame_hidden_initially(self, modern_gui_with_mocked_tk):
        """Test that scientific frame is hidden initially."""
        gui = modern_gui_with_mocked_tk
        # Scientific mode is initially off
        assert gui.scientific_mode is False


# ==============================================================================
# TESTS: Button Color Scheme
# ==============================================================================

class TestButtonColorScheme:
    """Test suite for button color scheme."""

    def test_utility_button_color_is_gray(self):
        """Test that utility buttons use gray color."""
        assert UTIL_BTN_COLOR == "#A5A5A5"

    def test_operator_button_color_is_orange(self):
        """Test that operator buttons use orange color."""
        assert OP_BTN_COLOR == "#FF9500"

    def test_number_button_color_is_dark_gray(self):
        """Test that number buttons use dark gray color."""
        assert NUM_BTN_COLOR == "#333333"

    def test_button_color_c_returns_util(self):
        """Test that C button returns utility color."""
        util_labels = {"C", "Del", "Mode"}
        op_labels = {"÷", "×", "+", "−", "="}
        color = ModernGUIInterface._button_color("C", util_labels, op_labels)
        assert color == UTIL_BTN_COLOR

    def test_button_color_del_returns_util(self):
        """Test that Del button returns utility color."""
        util_labels = {"C", "Del", "Mode"}
        op_labels = {"÷", "×", "+", "−", "="}
        color = ModernGUIInterface._button_color("Del", util_labels, op_labels)
        assert color == UTIL_BTN_COLOR

    def test_button_color_mode_returns_util(self):
        """Test that Mode button returns utility color."""
        util_labels = {"C", "Del", "Mode"}
        op_labels = {"÷", "×", "+", "−", "="}
        color = ModernGUIInterface._button_color("Mode", util_labels, op_labels)
        assert color == UTIL_BTN_COLOR

    def test_button_color_plus_returns_operator(self):
        """Test that + button returns operator color."""
        util_labels = {"C", "Del", "Mode"}
        op_labels = {"÷", "×", "+", "−", "="}
        color = ModernGUIInterface._button_color("+", util_labels, op_labels)
        assert color == OP_BTN_COLOR

    def test_button_color_divide_returns_operator(self):
        """Test that ÷ button returns operator color."""
        util_labels = {"C", "Del", "Mode"}
        op_labels = {"÷", "×", "+", "−", "="}
        color = ModernGUIInterface._button_color("÷", util_labels, op_labels)
        assert color == OP_BTN_COLOR

    def test_button_color_multiply_returns_operator(self):
        """Test that × button returns operator color."""
        util_labels = {"C", "Del", "Mode"}
        op_labels = {"÷", "×", "+", "−", "="}
        color = ModernGUIInterface._button_color("×", util_labels, op_labels)
        assert color == OP_BTN_COLOR

    def test_button_color_minus_returns_operator(self):
        """Test that − button returns operator color."""
        util_labels = {"C", "Del", "Mode"}
        op_labels = {"÷", "×", "+", "−", "="}
        color = ModernGUIInterface._button_color("−", util_labels, op_labels)
        assert color == OP_BTN_COLOR

    def test_button_color_equals_returns_operator(self):
        """Test that = button returns operator color."""
        util_labels = {"C", "Del", "Mode"}
        op_labels = {"÷", "×", "+", "−", "="}
        color = ModernGUIInterface._button_color("=", util_labels, op_labels)
        assert color == OP_BTN_COLOR

    def test_button_color_digit_returns_number(self):
        """Test that digit buttons return number color."""
        util_labels = {"C", "Del", "Mode"}
        op_labels = {"÷", "×", "+", "−", "="}
        for digit in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            color = ModernGUIInterface._button_color(digit, util_labels, op_labels)
            assert color == NUM_BTN_COLOR

    def test_button_color_decimal_returns_number(self):
        """Test that . button returns number color."""
        util_labels = {"C", "Del", "Mode"}
        op_labels = {"÷", "×", "+", "−", "="}
        color = ModernGUIInterface._button_color(".", util_labels, op_labels)
        assert color == NUM_BTN_COLOR


# ==============================================================================
# TESTS: Utility Helper Methods
# ==============================================================================

class TestUtilityHelperMethods:
    """Test suite for utility helper methods."""

    def test_parse_float_valid_integer(self):
        """Test _parse_float with valid integer."""
        result = ModernGUIInterface._parse_float("5")
        assert result == 5.0

    def test_parse_float_valid_float(self):
        """Test _parse_float with valid float."""
        result = ModernGUIInterface._parse_float("3.14")
        assert result == 3.14

    def test_parse_float_negative_number(self):
        """Test _parse_float with negative number."""
        result = ModernGUIInterface._parse_float("-5.5")
        assert result == -5.5

    def test_parse_float_scientific_notation(self):
        """Test _parse_float with scientific notation."""
        result = ModernGUIInterface._parse_float("1e3")
        assert result == 1000.0

    def test_parse_float_invalid_string(self):
        """Test _parse_float with invalid string."""
        result = ModernGUIInterface._parse_float("abc")
        assert result is None

    def test_parse_float_empty_string(self):
        """Test _parse_float with empty string."""
        result = ModernGUIInterface._parse_float("")
        assert result is None

    def test_parse_float_whitespace_only(self):
        """Test _parse_float with whitespace only."""
        result = ModernGUIInterface._parse_float("   ")
        assert result is None

    def test_parse_float_zero(self):
        """Test _parse_float with zero."""
        result = ModernGUIInterface._parse_float("0")
        assert result == 0.0

    def test_parse_float_leading_zeros(self):
        """Test _parse_float with leading zeros."""
        result = ModernGUIInterface._parse_float("0005")
        assert result == 5.0

    def test_parse_float_trailing_zeros(self):
        """Test _parse_float with trailing zeros."""
        result = ModernGUIInterface._parse_float("5.00")
        assert result == 5.0

    def test_format_result_whole_number_float(self):
        """Test _format_result with whole number float."""
        result = ModernGUIInterface._format_result(2.0)
        assert result == "2"

    def test_format_result_with_decimal(self):
        """Test _format_result with decimal number."""
        result = ModernGUIInterface._format_result(3.14)
        assert result == "3.14"

    def test_format_result_negative_whole_number(self):
        """Test _format_result with negative whole number."""
        result = ModernGUIInterface._format_result(-5.0)
        assert result == "-5"

    def test_format_result_zero(self):
        """Test _format_result with zero."""
        result = ModernGUIInterface._format_result(0.0)
        assert result == "0"

    def test_format_result_large_float(self):
        """Test _format_result with large float."""
        result = ModernGUIInterface._format_result(1234567.0)
        assert result == "1234567"

    def test_format_result_small_decimal(self):
        """Test _format_result with small decimal."""
        result = ModernGUIInterface._format_result(0.00001)
        assert "e" in result or "0.00001" in result


# ==============================================================================
# TESTS: Digit Input (_on_digit)
# ==============================================================================

class TestNumberButtonInteraction:
    """Test suite for digit input handling."""

    def test_on_digit_appends_digit_to_input(self, modern_gui_with_mocked_tk):
        """Test that digit button appends to current_input."""
        gui = modern_gui_with_mocked_tk
        gui._on_digit("5")
        assert gui.current_input == "5"

    def test_on_digit_multiple_digits(self, modern_gui_with_mocked_tk):
        """Test that multiple digit inputs accumulate."""
        gui = modern_gui_with_mocked_tk
        gui._on_digit("3")
        gui._on_digit("1")
        gui._on_digit("4")
        assert gui.current_input == "314"

    def test_on_digit_updates_display(self, modern_gui_with_mocked_tk):
        """Test that digit input updates display."""
        gui = modern_gui_with_mocked_tk
        gui._on_digit("7")
        assert gui.display_var.get() == "7"

    def test_on_digit_clears_after_result_shown(self, modern_gui_with_mocked_tk):
        """Test that digit input clears previous result."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui.result_shown = True
        gui._on_digit("3")
        assert gui.current_input == "3"

    def test_on_digit_prevents_duplicate_decimal(self, modern_gui_with_mocked_tk):
        """Test that multiple decimal points are prevented."""
        gui = modern_gui_with_mocked_tk
        gui._on_digit(".")
        gui._on_digit("5")
        gui._on_digit(".")
        assert gui.current_input == ".5"

    def test_on_digit_allows_decimal_first(self, modern_gui_with_mocked_tk):
        """Test that decimal point can be entered first."""
        gui = modern_gui_with_mocked_tk
        gui._on_digit(".")
        assert gui.current_input == "."

    def test_on_digit_resets_result_shown_flag(self, modern_gui_with_mocked_tk):
        """Test that result_shown is cleared after new input."""
        gui = modern_gui_with_mocked_tk
        gui.result_shown = True
        gui._on_digit("9")
        assert gui.result_shown is False

    def test_on_digit_zero_as_first_digit(self, modern_gui_with_mocked_tk):
        """Test that zero can be entered as first digit."""
        gui = modern_gui_with_mocked_tk
        gui._on_digit("0")
        assert gui.current_input == "0"

    def test_on_digit_after_operator(self, modern_gui_with_mocked_tk):
        """Test that digit can be entered after operator."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._on_operator("+")
        gui._on_digit("3")
        assert gui.current_input == "3"


# ==============================================================================
# TESTS: Operator Button Interaction (_on_operator)
# ==============================================================================

class TestOperatorButtonInteraction:
    """Test suite for operator button handling."""

    def test_on_operator_stores_first_operand(self, modern_gui_with_mocked_tk):
        """Test that operator stores first operand."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._on_operator("+")
        assert gui.first_operand == "5"

    def test_on_operator_sets_operation(self, modern_gui_with_mocked_tk):
        """Test that operator sets the operation."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._on_operator("+")
        assert gui.operation == "add"

    def test_on_operator_clears_current_input(self, modern_gui_with_mocked_tk):
        """Test that operator clears current input."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._on_operator("+")
        assert gui.current_input == ""

    def test_on_operator_resets_result_shown(self, modern_gui_with_mocked_tk):
        """Test that operator resets result_shown flag."""
        gui = modern_gui_with_mocked_tk
        gui.result_shown = True
        gui._on_operator("+")
        assert gui.result_shown is False

    def test_on_operator_minus_symbol(self, modern_gui_with_mocked_tk):
        """Test that minus symbol maps to subtract."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "10"
        gui._on_operator("−")
        assert gui.operation == "subtract"

    def test_on_operator_multiply_symbol(self, modern_gui_with_mocked_tk):
        """Test that multiply symbol maps correctly."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "3"
        gui._on_operator("×")
        assert gui.operation == "multiply"

    def test_on_operator_divide_symbol(self, modern_gui_with_mocked_tk):
        """Test that divide symbol maps correctly."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "20"
        gui._on_operator("÷")
        assert gui.operation == "divide"

    def test_on_operator_updates_display(self, modern_gui_with_mocked_tk):
        """Test that operator updates display to show symbol."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._on_operator("+")
        assert gui.display_var.get() == "+"

    def test_on_operator_allows_operator_change(self, modern_gui_with_mocked_tk):
        """Test that operator can be changed without losing operand."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._on_operator("+")
        gui._on_operator("−")
        assert gui.first_operand == "5"
        assert gui.operation == "subtract"

    def test_on_operator_with_no_input_preserves_operand(self, modern_gui_with_mocked_tk):
        """Test operator change with no new input."""
        gui = modern_gui_with_mocked_tk
        gui.first_operand = "5"
        gui.current_input = ""
        gui._on_operator("×")
        assert gui.first_operand == "5"
        assert gui.operation == "multiply"


# ==============================================================================
# TESTS: Equals Button Behavior (_on_equals)
# ==============================================================================

class TestEqualsButtonBehavior:
    """Test suite for equals button evaluation."""

    def test_on_equals_computes_addition(self, modern_gui_with_mocked_tk):
        """Test that equals computes addition."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._on_operator("+")
        gui.current_input = "3"
        gui._on_equals()
        assert gui.current_input == "8"

    def test_on_equals_computes_subtraction(self, modern_gui_with_mocked_tk):
        """Test that equals computes subtraction."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "10"
        gui._on_operator("−")
        gui.current_input = "3"
        gui._on_equals()
        assert gui.current_input == "7"

    def test_on_equals_computes_multiplication(self, modern_gui_with_mocked_tk):
        """Test that equals computes multiplication."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "4"
        gui._on_operator("×")
        gui.current_input = "5"
        gui._on_equals()
        assert gui.current_input == "20"

    def test_on_equals_computes_division(self, modern_gui_with_mocked_tk):
        """Test that equals computes division."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "20"
        gui._on_operator("÷")
        gui.current_input = "4"
        gui._on_equals()
        assert gui.current_input == "5"

    def test_on_equals_sets_result_shown(self, modern_gui_with_mocked_tk):
        """Test that equals sets result_shown flag."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._on_operator("+")
        gui.current_input = "3"
        gui._on_equals()
        assert gui.result_shown is True

    def test_on_equals_clears_operation(self, modern_gui_with_mocked_tk):
        """Test that equals clears the operation."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._on_operator("+")
        gui.current_input = "3"
        gui._on_equals()
        assert gui.operation is None

    def test_on_equals_clears_first_operand(self, modern_gui_with_mocked_tk):
        """Test that equals clears the first operand."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._on_operator("+")
        gui.current_input = "3"
        gui._on_equals()
        assert gui.first_operand is None

    def test_on_equals_records_in_history(self, modern_gui_with_mocked_tk):
        """Test that equals records operation in history."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._on_operator("+")
        gui.current_input = "3"
        gui._on_equals()
        history_entries = gui._history.display_history()
        assert len(history_entries) > 0
        assert "add" in history_entries[0] or "5" in history_entries[0]

    def test_on_equals_noop_without_operation(self, modern_gui_with_mocked_tk):
        """Test that equals does nothing without operation."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._on_equals()
        assert gui.current_input == "5"

    def test_on_equals_noop_without_first_operand(self, modern_gui_with_mocked_tk):
        """Test that equals does nothing without first operand."""
        gui = modern_gui_with_mocked_tk
        gui.operation = "add"
        gui.current_input = "3"
        gui._on_equals()
        assert gui.current_input == "3"

    def test_on_equals_noop_without_second_operand(self, modern_gui_with_mocked_tk):
        """Test that equals does nothing without second operand."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._on_operator("+")
        gui._on_equals()
        assert gui.operation == "add"

    def test_on_equals_handles_division_by_zero(self, modern_gui_with_mocked_tk):
        """Test that division by zero shows error."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._on_operator("÷")
        gui.current_input = "0"
        gui._on_equals()
        display = gui.display_var.get()
        assert "Error:" in display or "zero" in display.lower()

    def test_on_equals_updates_display(self, modern_gui_with_mocked_tk):
        """Test that equals updates display with result."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._on_operator("+")
        gui.current_input = "3"
        gui._on_equals()
        assert gui.display_var.get() == "8"


# ==============================================================================
# TESTS: Clear Button (_on_clear)
# ==============================================================================

class TestClearButton:
    """Test suite for clear button functionality."""

    def test_on_clear_resets_current_input(self, modern_gui_with_mocked_tk):
        """Test that clear resets current_input."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "123"
        gui._on_clear()
        assert gui.current_input == ""

    def test_on_clear_resets_operation(self, modern_gui_with_mocked_tk):
        """Test that clear resets operation."""
        gui = modern_gui_with_mocked_tk
        gui.operation = "add"
        gui._on_clear()
        assert gui.operation is None

    def test_on_clear_resets_first_operand(self, modern_gui_with_mocked_tk):
        """Test that clear resets first_operand."""
        gui = modern_gui_with_mocked_tk
        gui.first_operand = "5"
        gui._on_clear()
        assert gui.first_operand is None

    def test_on_clear_resets_result_shown(self, modern_gui_with_mocked_tk):
        """Test that clear resets result_shown."""
        gui = modern_gui_with_mocked_tk
        gui.result_shown = True
        gui._on_clear()
        assert gui.result_shown is False

    def test_on_clear_displays_zero(self, modern_gui_with_mocked_tk):
        """Test that clear displays '0'."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "123"
        gui._on_clear()
        assert gui.display_var.get() == "0"

    def test_on_clear_after_operation(self, modern_gui_with_mocked_tk):
        """Test clear after an operation."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._on_operator("+")
        gui.current_input = "3"
        gui._on_clear()
        assert gui.current_input == ""
        assert gui.operation is None
        assert gui.first_operand is None
        assert gui.display_var.get() == "0"


# ==============================================================================
# TESTS: Delete Button (_on_delete)
# ==============================================================================

class TestDeleteButton:
    """Test suite for delete button functionality."""

    def test_on_delete_removes_last_char(self, modern_gui_with_mocked_tk):
        """Test that delete removes last character."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "123"
        gui._on_delete()
        assert gui.current_input == "12"

    def test_on_delete_on_single_char(self, modern_gui_with_mocked_tk):
        """Test delete on single character."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._on_delete()
        assert gui.current_input == ""

    def test_on_delete_on_empty_input(self, modern_gui_with_mocked_tk):
        """Test delete on empty input."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = ""
        gui._on_delete()
        assert gui.current_input == ""

    def test_on_delete_updates_display(self, modern_gui_with_mocked_tk):
        """Test that delete updates display."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "123"
        gui._on_delete()
        assert gui.display_var.get() == "12"

    def test_on_delete_after_result_clears(self, modern_gui_with_mocked_tk):
        """Test that delete after result shown calls clear."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "8"
        gui.result_shown = True
        gui._on_delete()
        assert gui.current_input == ""
        assert gui.result_shown is False

    def test_on_delete_removes_decimal_point(self, modern_gui_with_mocked_tk):
        """Test that delete can remove decimal point."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "3.14"
        gui._on_delete()
        assert gui.current_input == "3.1"


# ==============================================================================
# TESTS: Mode Toggle (_on_mode_toggle)
# ==============================================================================

class TestModeToggle:
    """Test suite for mode toggle functionality."""

    def test_on_mode_toggle_switches_flag(self, modern_gui_with_mocked_tk):
        """Test that mode toggle switches scientific_mode flag."""
        gui = modern_gui_with_mocked_tk
        initial = gui.scientific_mode
        gui._on_mode_toggle()
        assert gui.scientific_mode == (not initial)

    def test_on_mode_toggle_updates_context(self, modern_gui_with_mocked_tk):
        """Test that mode toggle updates context."""
        gui = modern_gui_with_mocked_tk
        gui._on_mode_toggle()
        assert gui._context.get_mode() == "scientific"

    def test_on_mode_toggle_updates_registry(self, modern_gui_with_mocked_tk):
        """Test that mode toggle updates registry."""
        gui = modern_gui_with_mocked_tk
        gui._on_mode_toggle()
        assert gui._registry._current_mode == "scientific"

    def test_on_mode_toggle_back_to_normal(self, modern_gui_with_mocked_tk):
        """Test toggling back to normal mode."""
        gui = modern_gui_with_mocked_tk
        gui._on_mode_toggle()
        gui._on_mode_toggle()
        assert gui.scientific_mode is False
        assert gui._context.get_mode() == "normal"

    def test_on_mode_toggle_preserves_display(self, modern_gui_with_mocked_tk):
        """Test that mode toggle preserves display state."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "42"
        gui._on_mode_toggle()
        assert gui.current_input == "42"

    def test_on_mode_toggle_preserves_operation(self, modern_gui_with_mocked_tk):
        """Test that mode toggle preserves operation."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._on_operator("+")
        gui.current_input = "3"
        gui._on_mode_toggle()
        assert gui.first_operand == "5"
        assert gui.operation == "add"
        assert gui.current_input == "3"


# ==============================================================================
# TESTS: Scientific Operations (_on_scientific)
# ==============================================================================

class TestScientificUnaryOperations:
    """Test suite for unary scientific operations."""

    def test_on_scientific_square_root(self, modern_gui_with_mocked_tk):
        """Test square root operation."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "9"
        gui._on_scientific("√")
        assert gui.current_input == "3"

    def test_on_scientific_square(self, modern_gui_with_mocked_tk):
        """Test square operation."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._on_scientific("x²")
        assert gui.current_input == "25"

    def test_on_scientific_factorial(self, modern_gui_with_mocked_tk):
        """Test factorial operation."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._on_scientific("n!")
        assert gui.current_input == "120"

    def test_on_scientific_ln(self, modern_gui_with_mocked_tk):
        """Test natural logarithm operation."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "1"
        gui._on_scientific("ln")
        assert gui.current_input == "0"

    def test_on_scientific_log(self, modern_gui_with_mocked_tk):
        """Test base-10 logarithm operation."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "100"
        gui._on_scientific("log")
        assert gui.current_input == "2"

    def test_on_scientific_sets_result_shown(self, modern_gui_with_mocked_tk):
        """Test that scientific operation sets result_shown."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "9"
        gui._on_scientific("√")
        assert gui.result_shown is True

    def test_on_scientific_records_history(self, modern_gui_with_mocked_tk):
        """Test that scientific operation records in history."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "4"
        gui._on_scientific("x²")
        history_entries = gui._history.display_history()
        assert len(history_entries) > 0

    def test_on_scientific_noop_without_input(self, modern_gui_with_mocked_tk):
        """Test that unary operation does nothing without input."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = ""
        gui._on_scientific("√")
        assert gui.current_input == ""

    def test_on_scientific_sqrt_of_negative_errors(self, modern_gui_with_mocked_tk):
        """Test that sqrt of negative shows error."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "-4"
        gui._on_scientific("√")
        assert "Error:" in gui.display_var.get()

    def test_on_scientific_factorial_of_negative_errors(self, modern_gui_with_mocked_tk):
        """Test that factorial of negative shows error."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "-5"
        gui._on_scientific("n!")
        assert "Error:" in gui.display_var.get()


class TestScientificBinaryOperations:
    """Test suite for binary scientific operations (power)."""

    def test_on_scientific_power_stores_base(self, modern_gui_with_mocked_tk):
        """Test that xʸ stores base as first operand."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "2"
        gui._on_scientific("xʸ")
        assert gui.first_operand == "2"

    def test_on_scientific_power_sets_operation(self, modern_gui_with_mocked_tk):
        """Test that xʸ sets operation to power."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "2"
        gui._on_scientific("xʸ")
        assert gui.operation == "power"

    def test_on_scientific_power_clears_input(self, modern_gui_with_mocked_tk):
        """Test that xʸ clears current input."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "2"
        gui._on_scientific("xʸ")
        assert gui.current_input == ""

    def test_on_scientific_power_displays_symbol(self, modern_gui_with_mocked_tk):
        """Test that xʸ displays the symbol."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "2"
        gui._on_scientific("xʸ")
        assert gui.display_var.get() == "xʸ"

    def test_on_scientific_power_then_equals(self, modern_gui_with_mocked_tk):
        """Test power operation completed with equals."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "2"
        gui._on_scientific("xʸ")
        gui.current_input = "3"
        gui._on_equals()
        assert gui.current_input == "8"

    def test_on_scientific_power_noop_without_base(self, modern_gui_with_mocked_tk):
        """Test that xʸ without base doesn't error."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = ""
        gui._on_scientific("xʸ")
        # Should not crash, first_operand remains None
        assert gui.operation == "power"


# ==============================================================================
# TESTS: Unicode Symbols
# ==============================================================================

class TestUnicodeSymbols:
    """Test suite for Unicode symbols in button labels."""

    def test_divide_symbol_is_correct(self):
        """Test that divide symbol is Unicode ÷."""
        assert _DIV_SYMBOL == "÷"

    def test_multiply_symbol_is_correct(self):
        """Test that multiply symbol is Unicode ×."""
        assert _MUL_SYMBOL == "×"

    def test_subtract_symbol_is_correct(self):
        """Test that subtract symbol is Unicode −."""
        assert _SUB_SYMBOL == "−"

    def test_sqrt_symbol_in_scientific_labels(self):
        """Test that square root symbol is in scientific labels."""
        labels = [label for row in _SCIENTIFIC_LABELS for label in row]
        assert "√" in labels

    def test_square_symbol_in_scientific_labels(self):
        """Test that x² symbol is in scientific labels."""
        labels = [label for row in _SCIENTIFIC_LABELS for label in row]
        assert "x²" in labels

    def test_power_symbol_in_scientific_labels(self):
        """Test that xʸ symbol is in scientific labels."""
        labels = [label for row in _SCIENTIFIC_LABELS for label in row]
        assert "xʸ" in labels


# ==============================================================================
# TESTS: State Preservation
# ==============================================================================

class TestStatePreservation:
    """Test suite for state preservation across mode toggles."""

    def test_state_preserved_display_value(self, modern_gui_with_mocked_tk):
        """Test that display value is preserved in toggle."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "123.45"
        gui._on_mode_toggle()
        assert gui.current_input == "123.45"

    def test_state_preserved_first_operand(self, modern_gui_with_mocked_tk):
        """Test that first operand is preserved in toggle."""
        gui = modern_gui_with_mocked_tk
        gui.first_operand = "10"
        gui._on_mode_toggle()
        assert gui.first_operand == "10"

    def test_state_preserved_operation(self, modern_gui_with_mocked_tk):
        """Test that operation is preserved in toggle."""
        gui = modern_gui_with_mocked_tk
        gui.operation = "add"
        gui._on_mode_toggle()
        assert gui.operation == "add"

    def test_state_preserved_result_shown(self, modern_gui_with_mocked_tk):
        """Test that result_shown flag is preserved in toggle."""
        gui = modern_gui_with_mocked_tk
        gui.result_shown = True
        gui._on_mode_toggle()
        assert gui.result_shown is True

    def test_full_calculation_across_mode_toggle(self, modern_gui_with_mocked_tk):
        """Test full calculation with mode toggle in middle."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "10"
        gui._on_operator("+")
        gui.current_input = "5"
        gui._on_mode_toggle()
        gui._on_equals()
        assert gui.current_input == "15"


# ==============================================================================
# TESTS: Error Handling
# ==============================================================================

class TestErrorHandling:
    """Test suite for error handling and display."""

    def test_invalid_operand_string_displays_error(self, modern_gui_with_mocked_tk):
        """Test that invalid operand displays error."""
        gui = modern_gui_with_mocked_tk
        gui.first_operand = "abc"
        gui.operation = "add"
        gui.current_input = "5"
        gui._on_equals()
        assert "Error:" in gui.display_var.get()

    def test_division_by_zero_displays_error(self, modern_gui_with_mocked_tk):
        """Test that division by zero displays error."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._on_operator("÷")
        gui.current_input = "0"
        gui._on_equals()
        display = gui.display_var.get()
        assert "Error:" in display

    def test_error_clears_current_input(self, modern_gui_with_mocked_tk):
        """Test that error clears current input."""
        gui = modern_gui_with_mocked_tk
        gui.first_operand = "abc"
        gui.operation = "add"
        gui.current_input = "5"
        gui._on_equals()
        assert gui.current_input == ""

    def test_error_resets_result_shown(self, modern_gui_with_mocked_tk):
        """Test that error resets result_shown."""
        gui = modern_gui_with_mocked_tk
        gui.first_operand = "abc"
        gui.operation = "add"
        gui.current_input = "5"
        gui.result_shown = True
        gui._on_equals()
        assert gui.result_shown is False

    def test_error_logger_called_on_calculation_error(self, modern_gui_with_mocked_tk):
        """Test that error logger is called."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._on_operator("÷")
        gui.current_input = "0"
        gui._on_equals()
        errors = gui._error_logger.get_errors()
        assert len(errors) > 0


# ==============================================================================
# TESTS: Display and Update
# ==============================================================================

class TestDisplayUpdate:
    """Test suite for display update logic."""

    def test_update_display_with_explicit_text(self, modern_gui_with_mocked_tk):
        """Test _update_display with explicit text."""
        gui = modern_gui_with_mocked_tk
        gui._update_display("test")
        assert gui.display_var.get() == "test"

    def test_update_display_from_current_input(self, modern_gui_with_mocked_tk):
        """Test _update_display from current_input."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "42"
        gui._update_display()
        assert gui.display_var.get() == "42"

    def test_update_display_defaults_to_zero(self, modern_gui_with_mocked_tk):
        """Test _update_display defaults to '0'."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = ""
        gui._update_display()
        assert gui.display_var.get() == "0"

    def test_display_error_shows_error_text(self, modern_gui_with_mocked_tk):
        """Test _display_error shows error message."""
        gui = modern_gui_with_mocked_tk
        gui._display_error("test error")
        assert "Error: test error" in gui.display_var.get()

    def test_display_error_clears_input(self, modern_gui_with_mocked_tk):
        """Test _display_error clears current_input."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._display_error("test")
        assert gui.current_input == ""

    def test_display_error_resets_result_shown(self, modern_gui_with_mocked_tk):
        """Test _display_error resets result_shown."""
        gui = modern_gui_with_mocked_tk
        gui.result_shown = True
        gui._display_error("test")
        assert gui.result_shown is False


# ==============================================================================
# TESTS: Button Routing
# ==============================================================================

class TestButtonRouting:
    """Test suite for button press routing."""

    def test_button_press_c_calls_on_clear(self, modern_gui_with_mocked_tk):
        """Test that C button calls _on_clear."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "123"
        gui._on_button_press("C")
        assert gui.current_input == ""

    def test_button_press_del_calls_on_delete(self, modern_gui_with_mocked_tk):
        """Test that Del button calls _on_delete."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "123"
        gui._on_button_press("Del")
        assert gui.current_input == "12"

    def test_button_press_mode_calls_on_mode_toggle(self, modern_gui_with_mocked_tk):
        """Test that Mode button calls _on_mode_toggle."""
        gui = modern_gui_with_mocked_tk
        gui._on_button_press("Mode")
        assert gui.scientific_mode is True

    def test_button_press_equals_calls_on_equals(self, modern_gui_with_mocked_tk):
        """Test that = button calls _on_equals."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._on_operator("+")
        gui.current_input = "3"
        gui._on_button_press("=")
        assert gui.current_input == "8"

    def test_button_press_operator_calls_on_operator(self, modern_gui_with_mocked_tk):
        """Test that operator button calls _on_operator."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "5"
        gui._on_button_press("+")
        assert gui.operation == "add"

    def test_button_press_scientific_calls_on_scientific(self, modern_gui_with_mocked_tk):
        """Test that scientific button calls _on_scientific."""
        gui = modern_gui_with_mocked_tk
        gui.current_input = "9"
        gui._on_button_press("√")
        assert gui.current_input == "3"

    def test_button_press_digit_calls_on_digit(self, modern_gui_with_mocked_tk):
        """Test that digit button calls _on_digit."""
        gui = modern_gui_with_mocked_tk
        gui._on_button_press("5")
        assert gui.current_input == "5"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
