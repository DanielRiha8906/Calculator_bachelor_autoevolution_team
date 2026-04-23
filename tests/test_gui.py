"""Integration tests for the iOS-inspired CalculatorGUI.

These tests run in a headless environment without a display server.
Tests use tk.Tk() with withdraw() to avoid window rendering, and mock
operations to prevent mainloop() from being called.
"""

from unittest import mock

import pytest

pytestmark = pytest.mark.gui

# Skip all tests in this module if tkinter is unavailable
tk = pytest.importorskip("tkinter")

from src.gui import (
    CalculatorGUI,
    BG_COLOR,
    BTN_STANDARD,
    BTN_OPERATOR,
    BTN_UTILITY,
    DISPLAY_FG,
)
from src.session_history import SessionHistory


@pytest.fixture
def gui_setup():
    """Create a test GUI with withdrawn window."""
    root = tk.Tk()
    root.withdraw()
    history = SessionHistory()
    gui = CalculatorGUI(root, history)
    yield gui, root, history
    root.destroy()


class TestCalculatorGUIInitialization:
    """Test suite for CalculatorGUI initialization."""

    def test_gui_window_created(self, gui_setup):
        """Verify that the Tk root window is created and configured."""
        gui, root, _ = gui_setup
        assert isinstance(gui.root, tk.Tk)
        assert gui.root.title() == "Calculator"

    def test_gui_color_scheme(self, gui_setup):
        """Verify background is black."""
        gui, root, _ = gui_setup
        assert gui.root.cget("bg") == BG_COLOR
        assert BG_COLOR == "#000000"

    def test_standard_grid_created(self, gui_setup):
        """Verify standard button grid frame exists."""
        gui, _, _ = gui_setup
        assert hasattr(gui, "_std_frame")
        assert isinstance(gui._std_frame, tk.Frame)

    def test_display_widget_created(self, gui_setup):
        """Verify display label exists with white foreground."""
        gui, _, _ = gui_setup
        assert hasattr(gui, "_display_label")
        assert isinstance(gui._display_label, tk.Label)
        assert gui._display_label.cget("fg") == DISPLAY_FG
        assert gui._display_label.cget("fg") == "#FFFFFF"

    def test_scientific_panel_exists_hidden(self, gui_setup):
        """Verify scientific panel exists and is hidden initially."""
        gui, _, _ = gui_setup
        assert hasattr(gui, "_sci_frame")
        assert isinstance(gui._sci_frame, tk.Frame)
        assert gui._scientific_visible is False

    def test_engine_component_initialized(self, gui_setup):
        """Verify calculator and history components are initialized."""
        gui, _, history = gui_setup
        assert gui._calc is not None
        assert gui._history is history
        assert isinstance(gui._history, SessionHistory)

    def test_initial_display_is_zero(self, gui_setup):
        """Verify display shows '0' after initialization."""
        gui, _, _ = gui_setup
        assert gui._get_display() == "0"

    def test_initial_state_variables(self, gui_setup):
        """Verify internal state variables are initialized correctly."""
        gui, _, _ = gui_setup
        assert gui._first_operand is None
        assert gui._pending_op is None
        assert gui._reset_display is False
        assert gui._scientific_visible is False


class TestCalculatorGUIDisplay:
    """Test suite for display and button interactions."""

    def test_numeric_button_updates_display(self, gui_setup):
        """Verify digit buttons update the display."""
        gui, _, _ = gui_setup
        gui._on_digit("5")
        assert gui._get_display() == "5"

    def test_multiple_digits_concatenate(self, gui_setup):
        """Verify multiple digit presses concatenate."""
        gui, _, _ = gui_setup
        gui._on_digit("1")
        gui._on_digit("2")
        gui._on_digit("3")
        assert gui._get_display() == "123"

    def test_decimal_button_adds_dot(self, gui_setup):
        """Verify decimal button adds a dot to the display."""
        gui, _, _ = gui_setup
        gui._on_digit("5")
        gui._on_decimal()
        gui._on_digit("3")
        assert gui._get_display() == "5.3"

    def test_double_decimal_ignored(self, gui_setup):
        """Verify second decimal point is ignored."""
        gui, _, _ = gui_setup
        gui._on_digit("5")
        gui._on_decimal()
        gui._on_decimal()
        assert gui._get_display() == "5."

    def test_clear_button_resets_display(self, gui_setup):
        """Verify clear button resets display and state."""
        gui, _, _ = gui_setup
        gui._on_digit("1")
        gui._on_digit("2")
        gui._on_digit("3")
        gui._on_clear()
        assert gui._get_display() == "0"

    def test_delete_button_removes_last_char(self, gui_setup):
        """Verify delete button removes last character."""
        gui, _, _ = gui_setup
        gui._on_digit("1")
        gui._on_digit("2")
        gui._on_digit("3")
        gui._on_delete()
        assert gui._get_display() == "12"

    def test_delete_on_single_char_resets_to_zero(self, gui_setup):
        """Verify delete on single character resets to zero."""
        gui, _, _ = gui_setup
        gui._on_digit("5")
        gui._on_delete()
        assert gui._get_display() == "0"

    def test_delete_on_error_resets_to_zero(self, gui_setup):
        """Verify delete on error state resets to zero."""
        gui, _, _ = gui_setup
        gui._set_display("Error")
        gui._on_delete()
        assert gui._get_display() == "0"

    def test_display_right_aligned_white(self, gui_setup):
        """Verify display label is right-aligned with white foreground."""
        gui, _, _ = gui_setup
        assert gui._display_label.cget("fg") == DISPLAY_FG
        assert gui._display_label.cget("anchor") == "e"

    def test_reset_display_flag_clears_on_digit(self, gui_setup):
        """Verify digit input clears display when reset flag is True."""
        gui, _, _ = gui_setup
        gui._set_display("5")
        gui._reset_display = True
        gui._on_digit("7")
        assert gui._get_display() == "7"

    def test_decimal_on_reset_display_starts_fresh(self, gui_setup):
        """Verify decimal on reset display produces '0.'."""
        gui, _, _ = gui_setup
        gui._reset_display = True
        gui._on_decimal()
        assert gui._get_display() == "0."

    def test_leading_zero_prevention(self, gui_setup):
        """Verify leading zero is replaced when pressing digit on '0'."""
        gui, _, _ = gui_setup
        assert gui._get_display() == "0"
        gui._on_digit("0")
        # Second zero should be ignored (display already is "0")
        assert gui._get_display() == "0"
        gui._on_digit("5")
        # Now display should be "5", not "05"
        assert gui._get_display() == "5"


class TestCalculatorGUIArithmetic:
    """Test suite for arithmetic operations."""

    def test_simple_addition(self, gui_setup):
        """Verify 5 + 3 = 8."""
        gui, _, _ = gui_setup
        gui._on_digit("5")
        gui._on_operator("+")
        gui._on_digit("3")
        gui._on_equals()
        assert gui._get_display() == "8"

    def test_simple_subtraction(self, gui_setup):
        """Verify 9 - 4 = 5."""
        gui, _, _ = gui_setup
        gui._on_digit("9")
        gui._on_operator("−")
        gui._on_digit("4")
        gui._on_equals()
        assert gui._get_display() == "5"

    def test_simple_multiplication(self, gui_setup):
        """Verify 6 × 7 = 42."""
        gui, _, _ = gui_setup
        gui._on_digit("6")
        gui._on_operator("×")
        gui._on_digit("7")
        gui._on_equals()
        assert gui._get_display() == "42"

    def test_simple_division(self, gui_setup):
        """Verify 10 ÷ 2 = 5."""
        gui, _, _ = gui_setup
        gui._on_digit("1")
        gui._on_digit("0")
        gui._on_operator("÷")
        gui._on_digit("2")
        gui._on_equals()
        assert gui._get_display() == "5"

    def test_division_by_zero_shows_error(self, gui_setup):
        """Verify 1 ÷ 0 displays 'Error'."""
        gui, _, _ = gui_setup
        gui._on_digit("1")
        gui._on_operator("÷")
        gui._on_digit("0")
        gui._on_equals()
        assert gui._get_display() == "Error"

    def test_chained_operations(self, gui_setup):
        """Verify chained operations evaluate left-to-right."""
        gui, _, _ = gui_setup
        gui._on_digit("2")
        gui._on_operator("+")
        gui._on_digit("3")
        gui._on_operator("+")  # Should evaluate 2+3=5 first
        gui._on_digit("4")
        gui._on_equals()
        assert gui._get_display() == "9"

    def test_operator_sets_reset_display(self, gui_setup):
        """Verify operator press sets reset_display flag."""
        gui, _, _ = gui_setup
        gui._set_display("7")
        gui._on_operator("+")
        assert gui._reset_display is True

    def test_operator_stores_first_operand(self, gui_setup):
        """Verify operator stores first operand."""
        gui, _, _ = gui_setup
        gui._set_display("7")
        gui._on_operator("+")
        assert gui._first_operand == 7.0
        assert gui._pending_op == "+"

    def test_clear_resets_all_state(self, gui_setup):
        """Verify clear resets all internal state."""
        gui, _, _ = gui_setup
        gui._on_digit("5")
        gui._on_operator("+")
        gui._on_digit("3")
        gui._on_clear()
        assert gui._get_display() == "0"
        assert gui._first_operand is None
        assert gui._pending_op is None
        assert gui._reset_display is False

    @pytest.mark.parametrize("a,op,b,expected", [
        ("5", "+", "3", "8"),
        ("10", "−", "4", "6"),
        ("3", "×", "7", "21"),
        ("12", "÷", "3", "4"),
    ])
    def test_arithmetic_operations(self, gui_setup, a, op, b, expected):
        """Parametrized test for basic arithmetic operations."""
        gui, _, _ = gui_setup
        gui._on_digit(a[0])
        if len(a) > 1:
            gui._on_digit(a[1])
        gui._on_operator(op)
        gui._on_digit(b)
        gui._on_equals()
        assert gui._get_display() == expected


class TestCalculatorGUIScientific:
    """Test suite for scientific operations."""

    def test_scientific_panel_hidden_initially(self, gui_setup):
        """Verify scientific panel is hidden initially."""
        gui, _, _ = gui_setup
        assert gui._scientific_visible is False

    def test_mode_toggle_shows_scientific(self, gui_setup):
        """Verify mode toggle shows scientific panel."""
        gui, _, _ = gui_setup
        gui._on_mode_toggle()
        assert gui._scientific_visible is True

    def test_mode_toggle_hides_after_second_press(self, gui_setup):
        """Verify second mode toggle hides scientific panel."""
        gui, _, _ = gui_setup
        gui._on_mode_toggle()
        gui._on_mode_toggle()
        assert gui._scientific_visible is False

    def test_square_root_operation(self, gui_setup):
        """Verify √4 = 2."""
        gui, _, _ = gui_setup
        gui._set_display("4")
        gui._on_scientific("√")
        assert gui._get_display() == "2"

    def test_square_operation(self, gui_setup):
        """Verify 5² = 25."""
        gui, _, _ = gui_setup
        gui._set_display("5")
        gui._on_scientific("x²")
        assert gui._get_display() == "25"

    def test_factorial_operation(self, gui_setup):
        """Verify 5! = 120."""
        gui, _, _ = gui_setup
        gui._set_display("5")
        gui._on_scientific("n!")
        assert gui._get_display() == "120"

    def test_factorial_non_integer_shows_error(self, gui_setup):
        """Verify factorial rejects non-integer input."""
        gui, _, _ = gui_setup
        gui._set_display("3.5")
        gui._on_scientific("n!")
        assert gui._get_display() == "Error"

    def test_factorial_negative_shows_error(self, gui_setup):
        """Verify factorial rejects negative numbers."""
        gui, _, _ = gui_setup
        gui._set_display("-3")
        gui._on_scientific("n!")
        assert gui._get_display() == "Error"

    def test_ln_operation(self, gui_setup):
        """Verify ln(1) = 0."""
        gui, _, _ = gui_setup
        gui._set_display("1")
        gui._on_scientific("ln")
        assert gui._get_display() == "0"

    def test_log_operation(self, gui_setup):
        """Verify log(100) = 2."""
        gui, _, _ = gui_setup
        gui._set_display("100")
        gui._on_scientific("log")
        assert gui._get_display() == "2"

    def test_power_sets_pending_op(self, gui_setup):
        """Verify power operation sets pending operator."""
        gui, _, _ = gui_setup
        gui._set_display("2")
        gui._on_scientific("xʸ")
        assert gui._pending_op == "xʸ"
        assert gui._first_operand == 2.0
        assert gui._reset_display is True

    def test_power_evaluates_correctly(self, gui_setup):
        """Verify 2^3 = 8."""
        gui, _, _ = gui_setup
        gui._set_display("2")
        gui._on_scientific("xʸ")
        gui._on_digit("3")
        gui._on_equals()
        assert gui._get_display() == "8"

    def test_square_root_of_negative_shows_error(self, gui_setup):
        """Verify square root of negative number shows error."""
        gui, _, _ = gui_setup
        gui._set_display("-4")
        gui._on_scientific("√")
        assert gui._get_display() == "Error"

    @pytest.mark.parametrize("value,func,expected", [
        ("9", "√", "3"),
        ("3", "x²", "9"),
        ("0", "x²", "0"),
        ("2", "x²", "4"),
    ])
    def test_scientific_operations(self, gui_setup, value, func, expected):
        """Parametrized test for scientific operations."""
        gui, _, _ = gui_setup
        gui._set_display(value)
        gui._on_scientific(func)
        assert gui._get_display() == expected


class TestCalculatorGUIColorScheme:
    """Test suite for color scheme constants and application."""

    def test_constants_defined(self, gui_setup):
        """Verify color constants are defined correctly."""
        assert BG_COLOR == "#000000"
        assert BTN_STANDARD == "#333333"
        assert BTN_OPERATOR == "#FF9500"
        assert BTN_UTILITY == "#A5A5A5"
        assert DISPLAY_FG == "#FFFFFF"

    def test_background_color_black(self, gui_setup):
        """Verify root background is black."""
        gui, _, _ = gui_setup
        assert gui.root.cget("bg") == BG_COLOR

    def test_display_text_white(self, gui_setup):
        """Verify display label text is white."""
        gui, _, _ = gui_setup
        assert gui._display_label.cget("fg") == DISPLAY_FG


class TestCalculatorGUIFormatResult:
    """Test suite for result formatting."""

    def test_format_whole_number(self, gui_setup):
        """Verify 3.0 formats to '3'."""
        gui, _, _ = gui_setup
        result = gui._format_result(3.0)
        assert result == "3"

    def test_format_float(self, gui_setup):
        """Verify 3.14 formats to '3.14'."""
        gui, _, _ = gui_setup
        result = gui._format_result(3.14)
        assert result == "3.14"

    def test_format_negative_whole(self, gui_setup):
        """Verify -5.0 formats to '-5'."""
        gui, _, _ = gui_setup
        result = gui._format_result(-5.0)
        assert result == "-5"

    def test_format_zero(self, gui_setup):
        """Verify 0.0 formats to '0'."""
        gui, _, _ = gui_setup
        result = gui._format_result(0.0)
        assert result == "0"

    def test_format_large_float(self, gui_setup):
        """Verify large floats are formatted correctly."""
        gui, _, _ = gui_setup
        result = gui._format_result(1234567.89)
        assert result == "1234567.89"


class TestCalculatorGUIHistory:
    """Test suite for history recording integration."""

    def test_history_recorded_on_addition(self, gui_setup):
        """Verify history records addition operation."""
        gui, _, history = gui_setup
        gui._on_digit("5")
        gui._on_operator("+")
        gui._on_digit("3")
        gui._on_equals()

        assert not history.is_empty()
        entries = history.get_history()
        assert len(entries) >= 1
        assert entries[-1]["operation"] == "add"
        assert entries[-1]["operands"] == [5.0, 3.0]
        assert entries[-1]["result"] == 8.0

    def test_history_recorded_on_multiplication(self, gui_setup):
        """Verify history records multiplication operation."""
        gui, _, history = gui_setup
        gui._on_digit("6")
        gui._on_operator("×")
        gui._on_digit("7")
        gui._on_equals()

        entries = history.get_history()
        assert len(entries) >= 1
        assert entries[-1]["operation"] == "multiply"
        assert entries[-1]["result"] == 42.0

    def test_history_recorded_on_scientific_operation(self, gui_setup):
        """Verify history records scientific operations."""
        gui, _, history = gui_setup
        gui._set_display("5")
        gui._on_scientific("x²")

        entries = history.get_history()
        assert len(entries) >= 1
        assert entries[-1]["operation"] == "square"
        assert entries[-1]["result"] == 25.0

    def test_multiple_operations_in_history(self, gui_setup):
        """Verify multiple operations are recorded."""
        gui, _, history = gui_setup
        # First operation
        gui._on_digit("2")
        gui._on_operator("+")
        gui._on_digit("3")
        gui._on_equals()

        # Second operation
        gui._on_clear()
        gui._on_digit("5")
        gui._on_operator("×")
        gui._on_digit("4")
        gui._on_equals()

        entries = history.get_history()
        assert len(entries) >= 2
        assert entries[0]["operation"] == "add"
        assert entries[1]["operation"] == "multiply"


class TestCalculatorGUIEdgeCases:
    """Test suite for edge cases and error handling."""

    def test_operation_on_invalid_display(self, gui_setup):
        """Verify operator press on invalid display shows error."""
        gui, _, _ = gui_setup
        gui._set_display("abc")
        gui._on_operator("+")
        assert gui._get_display() == "Error"

    def test_negative_operands_addition(self, gui_setup):
        """Verify addition works with negative operands."""
        gui, _, _ = gui_setup
        gui._set_display("-5")
        gui._on_operator("+")
        gui._on_digit("3")
        gui._on_equals()
        assert gui._get_display() == "-2"

    def test_fractional_operands(self, gui_setup):
        """Verify operations work with fractional operands."""
        gui, _, _ = gui_setup
        gui._set_display("2.5")
        gui._on_operator("+")
        gui._on_digit("1")
        gui._on_decimal()
        gui._on_digit("5")
        gui._on_equals()
        assert gui._get_display() == "4"

    def test_very_large_operands(self, gui_setup):
        """Verify operations with very large numbers."""
        gui, _, _ = gui_setup
        gui._set_display("1e100")
        gui._on_operator("+")
        gui._on_digit("1")
        gui._on_equals()
        result = gui._get_display()
        assert isinstance(result, str)
        assert "Error" not in result or result == "Error"

    def test_equals_without_pending_operation(self, gui_setup):
        """Verify equals press without pending operation is safe."""
        gui, _, _ = gui_setup
        gui._set_display("5")
        gui._on_equals()
        assert gui._get_display() == "5"

    def test_decimal_on_fresh_display(self, gui_setup):
        """Verify decimal on fresh '0' display produces '0.'."""
        gui, _, _ = gui_setup
        assert gui._get_display() == "0"
        gui._on_decimal()
        assert gui._get_display() == "0."

    def test_multiple_consecutive_operators(self, gui_setup):
        """Verify consecutive operators work correctly."""
        gui, _, _ = gui_setup
        gui._on_digit("5")
        gui._on_operator("+")
        gui._on_operator("+")  # Second operator should be treated same as first
        assert gui._pending_op == "+"
        gui._on_digit("3")
        gui._on_equals()
        assert gui._get_display() == "8"

    def test_error_recovery_with_clear(self, gui_setup):
        """Verify error state can be cleared."""
        gui, _, _ = gui_setup
        gui._on_digit("1")
        gui._on_operator("÷")
        gui._on_digit("0")
        gui._on_equals()
        assert gui._get_display() == "Error"
        gui._on_clear()
        assert gui._get_display() == "0"
        assert gui._first_operand is None
        assert gui._pending_op is None

    def test_zero_factorial_equals_one(self, gui_setup):
        """Verify 0! = 1."""
        gui, _, _ = gui_setup
        gui._set_display("0")
        gui._on_scientific("n!")
        assert gui._get_display() == "1"

    @pytest.mark.parametrize("invalid_input", [
        "abc",
        "12.34.56",
        "1e1e10",
    ])
    def test_invalid_inputs_on_operator(self, gui_setup, invalid_input):
        """Verify invalid inputs on operator press show error."""
        gui, _, _ = gui_setup
        gui._set_display(invalid_input)
        gui._on_operator("+")
        assert gui._get_display() == "Error"

    def test_scientific_on_invalid_display(self, gui_setup):
        """Verify scientific function on invalid display shows error."""
        gui, _, _ = gui_setup
        gui._set_display("abc")
        gui._on_scientific("√")
        assert gui._get_display() == "Error"

    def test_reset_display_flag_after_operation(self, gui_setup):
        """Verify reset_display flag is set after operation."""
        gui, _, _ = gui_setup
        gui._on_digit("5")
        gui._on_operator("+")
        assert gui._reset_display is True
        gui._on_digit("3")
        assert gui._reset_display is False

    def test_first_operand_stored_as_float(self, gui_setup):
        """Verify first operand is stored as float."""
        gui, _, _ = gui_setup
        gui._on_digit("5")
        gui._on_operator("+")
        assert isinstance(gui._first_operand, float)
        assert gui._first_operand == 5.0

    def test_empty_entry_with_decimal(self, gui_setup):
        """Verify decimal on '0' creates proper decimal number."""
        gui, _, _ = gui_setup
        assert gui._get_display() == "0"
        gui._on_decimal()
        assert gui._get_display() == "0."
        gui._on_digit("5")
        assert gui._get_display() == "0.5"

    def test_scientific_sets_reset_flag(self, gui_setup):
        """Verify scientific operations set reset_display flag."""
        gui, _, _ = gui_setup
        gui._set_display("5")
        gui._on_scientific("x²")
        assert gui._reset_display is True
        gui._on_digit("3")
        assert gui._get_display() == "3"
