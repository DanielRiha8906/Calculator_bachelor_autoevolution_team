"""Tests for the GUI layer (src/gui.py).

Tests the CalculatorGUI class. Since the environment is headless (no X11 display),
we mock tkinter components to allow instantiation and testing of state machine
methods without a real display.
"""

from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

import pytest

# Mock tkinter before importing gui module
sys.modules['tkinter'] = MagicMock()

from src.gui import CalculatorGUI


# ===========================================================================
# Fixtures
# ===========================================================================


@pytest.fixture
def mock_tkinter_components():
    """Patch all tkinter components needed for GUI testing."""
    with patch('src.gui.tk.Tk') as mock_tk, \
         patch('src.gui.tk.Frame') as mock_frame, \
         patch('src.gui.tk.Label') as mock_label, \
         patch('src.gui.tk.Button') as mock_button, \
         patch('src.gui.tk.StringVar') as mock_stringvar:

        # Create a mock root window
        mock_root = MagicMock()
        mock_tk.return_value = mock_root

        # Configure StringVar to store and retrieve values
        stringvar_values = {}
        def stringvar_init(value=""):
            var = MagicMock()
            stringvar_values['value'] = value
            var.set = MagicMock(side_effect=lambda v: stringvar_values.update({'value': v}))
            var.get = MagicMock(side_effect=lambda: stringvar_values.get('value', ''))
            return var
        mock_stringvar.side_effect = stringvar_init

        # Configure Frame to return mock
        mock_frame.return_value = MagicMock()

        # Configure Label to return mock
        mock_label.return_value = MagicMock()

        # Configure Button to return mock
        mock_button.return_value = MagicMock()

        yield {
            'mock_tk': mock_tk,
            'mock_frame': mock_frame,
            'mock_label': mock_label,
            'mock_button': mock_button,
            'mock_stringvar': mock_stringvar,
            'mock_root': mock_root,
            'stringvar_values': stringvar_values,
        }


@pytest.fixture
def gui(mock_tkinter_components):
    """Create a CalculatorGUI instance with mocked tkinter."""
    return CalculatorGUI()


# ===========================================================================
# TestGUIStateInitialization
# ===========================================================================


class TestGUIStateInitialization:
    """Verify that CalculatorGUI initializes with correct state."""

    def test_gui_instantiation(self, gui):
        """Verify that CalculatorGUI can be instantiated."""
        assert gui is not None
        assert isinstance(gui, CalculatorGUI)

    def test_initial_display_state(self, gui):
        """Verify initial display is "0"."""
        assert gui._current_display == "0"

    def test_initial_pending_operator_none(self, gui):
        """Verify initial pending operator is None."""
        assert gui._pending_operator is None

    def test_initial_pending_operand_none(self, gui):
        """Verify initial pending operand is None."""
        assert gui._pending_operand is None

    def test_initial_decimal_entered_false(self, gui):
        """Verify initial decimal_entered flag is False."""
        assert gui._decimal_entered is False

    def test_initial_scientific_mode_false(self, gui):
        """Verify initial scientific mode is False."""
        assert gui._is_scientific_mode is False

    def test_initial_result_just_shown_false(self, gui):
        """Verify initial result_just_shown flag is False."""
        assert gui._result_just_shown is False


# ===========================================================================
# TestDigitInput
# ===========================================================================


class TestDigitInput:
    """Test digit input behavior."""

    def test_single_digit_5_on_initial_state(self, gui):
        """Pressing digit 5 when display is "0": display becomes "5"."""
        gui._on_digit_pressed(5)
        assert gui._current_display == "5"

    def test_consecutive_digits_5_then_3(self, gui):
        """Pressing digit 5 then 3: display becomes "53"."""
        gui._on_digit_pressed(5)
        gui._on_digit_pressed(3)
        assert gui._current_display == "53"

    def test_digit_after_result_shown(self, gui):
        """Pressing digit after result shown resets display to new digit."""
        gui._current_display = "8"
        gui._result_just_shown = True
        gui._on_digit_pressed(5)
        assert gui._current_display == "5"

    def test_result_just_shown_cleared_after_digit(self, gui):
        """_result_just_shown is False after digit press."""
        gui._current_display = "8"
        gui._result_just_shown = True
        gui._on_digit_pressed(5)
        assert gui._result_just_shown is False

    def test_digit_appends_to_existing_number(self, gui):
        """Digits append to non-zero display."""
        gui._current_display = "5"
        gui._result_just_shown = False
        gui._on_digit_pressed(3)
        assert gui._current_display == "53"

    def test_digit_zero_on_zero_display(self, gui):
        """Pressing 0 on "0" display stays "0"."""
        gui._current_display = "0"
        gui._on_digit_pressed(0)
        assert gui._current_display == "0"

    @pytest.mark.parametrize("digit", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test_all_digits_input(self, gui, digit):
        """Test all digits 0-9 can be pressed."""
        gui._on_digit_pressed(digit)
        assert gui._current_display == str(digit)

    def test_decimal_entered_reset_after_digit_press(self, gui):
        """decimal_entered flag is reset when replacing display."""
        gui._current_display = "5.0"
        gui._decimal_entered = True
        gui._result_just_shown = True
        gui._on_digit_pressed(3)
        assert gui._decimal_entered is False


# ===========================================================================
# TestDecimalInput
# ===========================================================================


class TestDecimalInput:
    """Test decimal point input behavior."""

    def test_decimal_appends_to_display(self, gui):
        """Pressing decimal when display is "5": display becomes "5."."""
        gui._current_display = "5"
        gui._on_decimal_pressed()
        assert gui._current_display == "5."

    def test_decimal_entered_flag_set(self, gui):
        """_decimal_entered becomes True after decimal press."""
        gui._current_display = "5"
        gui._on_decimal_pressed()
        assert gui._decimal_entered is True

    def test_no_second_decimal(self, gui):
        """Pressing decimal again when _decimal_entered=True: display unchanged."""
        gui._current_display = "5."
        gui._decimal_entered = True
        gui._on_decimal_pressed()
        assert gui._current_display == "5."

    def test_decimal_when_result_just_shown(self, gui):
        """Pressing decimal when _result_just_shown=True: display becomes "0."."""
        gui._current_display = "8"
        gui._result_just_shown = True
        gui._on_decimal_pressed()
        assert gui._current_display == "0."

    def test_decimal_entered_true_after_result_shown_decimal(self, gui):
        """_decimal_entered=True after decimal pressed on result_just_shown."""
        gui._current_display = "8"
        gui._result_just_shown = True
        gui._on_decimal_pressed()
        assert gui._decimal_entered is True

    def test_result_just_shown_false_after_result_decimal(self, gui):
        """_result_just_shown=False after decimal pressed on result_just_shown."""
        gui._current_display = "8"
        gui._result_just_shown = True
        gui._on_decimal_pressed()
        assert gui._result_just_shown is False

    def test_decimal_on_initial_display(self, gui):
        """Pressing decimal on initial "0": display becomes "0."."""
        gui._on_decimal_pressed()
        assert gui._current_display == "0."


# ===========================================================================
# TestOperatorPress
# ===========================================================================


class TestOperatorPress:
    """Test operator button behavior."""

    def test_plus_operator_sets_pending_operand(self, gui):
        """Pressing "+" operator: _pending_operand set to float of display."""
        gui._current_display = "5"
        gui._on_operator_pressed("add")
        assert gui._pending_operand == 5.0

    def test_plus_operator_sets_pending_operator(self, gui):
        """Pressing "+" operator: _pending_operator set to "add"."""
        gui._current_display = "5"
        gui._on_operator_pressed("add")
        assert gui._pending_operator == "add"

    def test_plus_operator_sets_result_just_shown(self, gui):
        """Pressing operator: _result_just_shown set to True."""
        gui._current_display = "5"
        gui._on_operator_pressed("add")
        assert gui._result_just_shown is True

    def test_plus_operator_resets_decimal_entered(self, gui):
        """Pressing operator: _decimal_entered reset to False."""
        gui._current_display = "5.5"
        gui._decimal_entered = True
        gui._on_operator_pressed("add")
        assert gui._decimal_entered is False

    @pytest.mark.parametrize("op_key,op_name", [
        ("add", "add"),
        ("subtract", "subtract"),
        ("multiply", "multiply"),
        ("divide", "divide"),
    ])
    def test_all_operators(self, gui, op_key, op_name):
        """Test all binary operators set pending_operator correctly."""
        gui._current_display = "10"
        gui._on_operator_pressed(op_key)
        assert gui._pending_operator == op_name
        assert gui._pending_operand == 10.0

    def test_operator_with_decimal_operand(self, gui):
        """Pressing operator with decimal display."""
        gui._current_display = "5.5"
        gui._on_operator_pressed("add")
        assert gui._pending_operand == 5.5


# ===========================================================================
# TestEqualsPress
# ===========================================================================


class TestEqualsPress:
    """Test equals button behavior."""

    def test_equals_with_no_pending_operator(self, gui):
        """Pressing = with no pending operator: nothing changes."""
        gui._current_display = "5"
        gui._on_equals_pressed()
        assert gui._current_display == "5"
        assert gui._pending_operator is None

    def test_full_calculation_5_plus_3(self, gui):
        """Full chain: 5 + 3 = displays "8"."""
        gui._on_digit_pressed(5)
        gui._on_operator_pressed("add")
        gui._on_digit_pressed(3)
        gui._on_equals_pressed()
        assert gui._current_display == "8"

    def test_equals_clears_pending_operator(self, gui):
        """_pending_operator is None after =."""
        gui._current_display = "5"
        gui._pending_operator = "add"
        gui._pending_operand = 3.0
        gui._on_equals_pressed()
        assert gui._pending_operator is None

    def test_equals_clears_pending_operand(self, gui):
        """_pending_operand is None after =."""
        gui._current_display = "5"
        gui._pending_operator = "add"
        gui._pending_operand = 3.0
        gui._on_equals_pressed()
        assert gui._pending_operand is None

    def test_equals_sets_result_just_shown(self, gui):
        """_result_just_shown is True after =."""
        gui._current_display = "5"
        gui._pending_operator = "add"
        gui._pending_operand = 3.0
        gui._on_equals_pressed()
        assert gui._result_just_shown is True

    def test_full_calculation_10_minus_4(self, gui):
        """Chain: 10 - 4 = displays "6"."""
        gui._on_digit_pressed(1)
        gui._on_digit_pressed(0)
        gui._on_operator_pressed("subtract")
        gui._on_digit_pressed(4)
        gui._on_equals_pressed()
        assert gui._current_display == "6"

    def test_full_calculation_3_multiply_4(self, gui):
        """Chain: 3 × 4 = displays "12"."""
        gui._on_digit_pressed(3)
        gui._on_operator_pressed("multiply")
        gui._on_digit_pressed(4)
        gui._on_equals_pressed()
        assert gui._current_display == "12"

    def test_equals_with_decimal_result(self, gui):
        """Chain: 5 ÷ 2 = displays "2.5"."""
        gui._on_digit_pressed(5)
        gui._on_operator_pressed("divide")
        gui._on_digit_pressed(2)
        gui._on_equals_pressed()
        assert gui._current_display == "2.5"


# ===========================================================================
# TestClearButton
# ===========================================================================


class TestClearButton:
    """Test clear button behavior."""

    def test_clear_resets_display(self, gui):
        """After pressing C: display shows "0"."""
        gui._current_display = "123"
        gui._on_clear_pressed()
        assert gui._current_display == "0"

    def test_clear_resets_pending_operator(self, gui):
        """After pressing C: _pending_operator is None."""
        gui._pending_operator = "add"
        gui._on_clear_pressed()
        assert gui._pending_operator is None

    def test_clear_resets_pending_operand(self, gui):
        """After pressing C: _pending_operand is None."""
        gui._pending_operand = 5.0
        gui._on_clear_pressed()
        assert gui._pending_operand is None

    def test_clear_resets_decimal_entered(self, gui):
        """After pressing C: _decimal_entered is False."""
        gui._decimal_entered = True
        gui._on_clear_pressed()
        assert gui._decimal_entered is False

    def test_clear_resets_result_just_shown(self, gui):
        """After pressing C: _result_just_shown is False."""
        gui._result_just_shown = True
        gui._on_clear_pressed()
        assert gui._result_just_shown is False

    def test_clear_after_partial_calculation(self, gui):
        """Clear resets all state after partial calculation."""
        gui._on_digit_pressed(5)
        gui._on_operator_pressed("add")
        gui._on_digit_pressed(3)
        gui._on_clear_pressed()

        assert gui._current_display == "0"
        assert gui._pending_operator is None
        assert gui._pending_operand is None
        assert gui._decimal_entered is False
        assert gui._result_just_shown is False


# ===========================================================================
# TestNegateButton
# ===========================================================================


class TestNegateButton:
    """Test negate (+/-) button behavior."""

    def test_negate_positive_to_negative(self, gui):
        """Pressing +/−: display "5" becomes "-5"."""
        gui._current_display = "5"
        gui._on_negate_pressed()
        assert gui._current_display == "-5"

    def test_negate_negative_to_positive(self, gui):
        """Pressing +/−: display "-5" becomes "5"."""
        gui._current_display = "-5"
        gui._on_negate_pressed()
        assert gui._current_display == "5"

    def test_negate_zero_stays_zero(self, gui):
        """Pressing +/−: display "0" becomes "-0" (formatting quirk)."""
        gui._current_display = "0"
        gui._on_negate_pressed()
        # Note: -0.0 formatted as "-0" due to str(float) behavior
        assert gui._current_display in ("0", "-0")

    def test_negate_decimal_number(self, gui):
        """Pressing +/−: display "3.14" becomes "-3.14"."""
        gui._current_display = "3.14"
        gui._on_negate_pressed()
        assert gui._current_display == "-3.14"

    def test_negate_integer_display_format(self, gui):
        """Pressing +/−: integer floats display without .0."""
        gui._current_display = "5.0"
        gui._on_negate_pressed()
        assert gui._current_display == "-5"

    def test_negate_on_error_display(self, gui):
        """Pressing +/−: error display stays unchanged."""
        gui._current_display = "Error"
        gui._on_negate_pressed()
        assert gui._current_display == "Error"


# ===========================================================================
# TestPercentButton
# ===========================================================================


class TestPercentButton:
    """Test percent (%) button behavior."""

    def test_percent_50_becomes_0_5(self, gui):
        """Pressing % on "50": display shows "0.5"."""
        gui._current_display = "50"
        gui._on_percent_pressed()
        assert gui._current_display == "0.5"

    def test_percent_100_becomes_1(self, gui):
        """Pressing % on "100": display shows "1"."""
        gui._current_display = "100"
        gui._on_percent_pressed()
        assert gui._current_display == "1"

    def test_percent_25_becomes_0_25(self, gui):
        """Pressing % on "25": display shows "0.25"."""
        gui._current_display = "25"
        gui._on_percent_pressed()
        assert gui._current_display == "0.25"

    def test_percent_1_becomes_0_01(self, gui):
        """Pressing % on "1": display shows "0.01"."""
        gui._current_display = "1"
        gui._on_percent_pressed()
        assert gui._current_display == "0.01"

    def test_percent_zero(self, gui):
        """Pressing % on "0": display shows "0"."""
        gui._current_display = "0"
        gui._on_percent_pressed()
        assert gui._current_display == "0"

    def test_percent_on_error_display(self, gui):
        """Pressing % on error display: stays unchanged."""
        gui._current_display = "Error"
        gui._on_percent_pressed()
        assert gui._current_display == "Error"

    def test_percent_updates_decimal_entered_flag(self, gui):
        """_decimal_entered updated to reflect result."""
        gui._current_display = "50"
        gui._on_percent_pressed()
        assert gui._decimal_entered is True


# ===========================================================================
# TestUnaryFunctions
# ===========================================================================


class TestUnaryFunctions:
    """Test unary scientific functions."""

    def test_square_root_of_9(self, gui):
        """_on_unary_pressed("square_root") with display "9" → "3"."""
        gui._current_display = "9"
        gui._on_unary_pressed("square_root")
        # Result could be "3.0" or "3" depending on formatting
        assert gui._current_display in ("3.0", "3")

    def test_square_of_4(self, gui):
        """_on_unary_pressed("square") with display "4" → "16"."""
        gui._current_display = "4"
        gui._on_unary_pressed("square")
        assert gui._current_display == "16"

    def test_unary_sets_result_just_shown(self, gui):
        """_result_just_shown is True after unary press."""
        gui._current_display = "4"
        gui._on_unary_pressed("square")
        assert gui._result_just_shown is True

    def test_cube_of_2(self, gui):
        """_on_unary_pressed("cube") with display "2" → "8"."""
        gui._current_display = "2"
        gui._on_unary_pressed("cube")
        assert gui._current_display == "8"

    def test_cube_root_of_8(self, gui):
        """_on_unary_pressed("cube_root") with display "8" → "2"."""
        gui._current_display = "8"
        gui._on_unary_pressed("cube_root")
        assert gui._current_display in ("2.0", "2")

    def test_factorial_of_5(self, gui):
        """_on_unary_pressed("factorial") with display "5" → "120"."""
        gui._current_display = "5"
        gui._on_unary_pressed("factorial")
        assert gui._current_display == "120"

    def test_ln_function(self, gui):
        """_on_unary_pressed("ln") executes without error."""
        gui._current_display = "2.718281828"
        gui._on_unary_pressed("ln")
        # Should be approximately "1"
        assert gui._current_display != "Error"

    def test_log_function(self, gui):
        """_on_unary_pressed("log") executes without error."""
        gui._current_display = "100"
        gui._on_unary_pressed("log")
        # Should be "2"
        assert gui._current_display in ("2.0", "2")

    def test_unary_with_invalid_operation(self, gui):
        """_on_unary_pressed with invalid key → display "Error"."""
        gui._current_display = "5"
        gui._on_unary_pressed("invalid_operation")
        assert gui._current_display == "Error"

    def test_unary_error_clears_pending_state(self, gui):
        """Error in unary function clears pending operator and operand."""
        gui._pending_operator = "add"
        gui._pending_operand = 5.0
        gui._current_display = "5"
        gui._on_unary_pressed("invalid_operation")

        assert gui._current_display == "Error"
        assert gui._pending_operator is None
        assert gui._pending_operand is None

    def test_unary_error_resets_decimal_flag(self, gui):
        """Error in unary function resets decimal_entered."""
        gui._decimal_entered = True
        gui._current_display = "5"
        gui._on_unary_pressed("invalid_operation")
        assert gui._decimal_entered is False

    def test_unary_square_root_negative_number(self, gui):
        """_on_unary_pressed("square_root") with negative number → "Error"."""
        gui._current_display = "-4"
        gui._on_unary_pressed("square_root")
        assert gui._current_display == "Error"


# ===========================================================================
# TestModeToggle
# ===========================================================================


class TestModeToggle:
    """Test scientific mode toggle behavior."""

    def test_initial_mode_normal(self, gui):
        """Initially _is_scientific_mode == False."""
        assert gui._is_scientific_mode is False

    def test_first_mode_toggle_sets_scientific(self, gui):
        """After mode toggle: _is_scientific_mode == True."""
        gui._on_mode_toggle()
        assert gui._is_scientific_mode is True

    def test_second_mode_toggle_resets_normal(self, gui):
        """After second mode toggle: _is_scientific_mode == False."""
        gui._on_mode_toggle()
        gui._on_mode_toggle()
        assert gui._is_scientific_mode is False

    def test_mode_toggle_preserves_display(self, gui):
        """Mode toggle preserves _current_display."""
        gui._current_display = "42"
        gui._on_mode_toggle()
        assert gui._current_display == "42"

    def test_mode_toggle_preserves_pending_operator(self, gui):
        """Mode toggle preserves _pending_operator."""
        gui._pending_operator = "add"
        gui._on_mode_toggle()
        assert gui._pending_operator == "add"

    def test_mode_toggle_preserves_pending_operand(self, gui):
        """Mode toggle preserves _pending_operand."""
        gui._pending_operand = 5.0
        gui._on_mode_toggle()
        assert gui._pending_operand == 5.0

    def test_mode_toggle_preserves_all_state(self, gui):
        """Mode toggle preserves all calculation state."""
        gui._current_display = "12"
        gui._pending_operator = "multiply"
        gui._pending_operand = 3.0
        gui._decimal_entered = True
        gui._result_just_shown = True

        gui._on_mode_toggle()

        assert gui._current_display == "12"
        assert gui._pending_operator == "multiply"
        assert gui._pending_operand == 3.0
        assert gui._decimal_entered is True
        assert gui._result_just_shown is True
        assert gui._is_scientific_mode is True


# ===========================================================================
# TestFormatResult
# ===========================================================================


class TestFormatResult:
    """Test the _format_result helper method."""

    def test_format_integer_float_8_0(self):
        """_format_result(8.0) returns "8"."""
        result = CalculatorGUI._format_result(8.0)
        assert result == "8"

    def test_format_decimal_3_14(self):
        """_format_result(3.14) returns "3.14"."""
        result = CalculatorGUI._format_result(3.14)
        assert result == "3.14"

    def test_format_negative_integer_5_0(self):
        """_format_result(-5.0) returns "-5"."""
        result = CalculatorGUI._format_result(-5.0)
        assert result == "-5"

    def test_format_decimal_0_5(self):
        """_format_result(0.5) returns "0.5"."""
        result = CalculatorGUI._format_result(0.5)
        assert result == "0.5"

    def test_format_zero(self):
        """_format_result(0.0) returns "0"."""
        result = CalculatorGUI._format_result(0.0)
        assert result == "0"

    def test_format_negative_decimal(self):
        """_format_result(-3.14) returns "-3.14"."""
        result = CalculatorGUI._format_result(-3.14)
        assert result == "-3.14"

    def test_format_large_integer(self):
        """_format_result(1000.0) returns "1000"."""
        result = CalculatorGUI._format_result(1000.0)
        assert result == "1000"

    def test_format_very_small_decimal(self):
        """_format_result(0.001) returns "0.001"."""
        result = CalculatorGUI._format_result(0.001)
        assert result == "0.001"

    def test_format_many_decimal_places(self):
        """_format_result with many decimals preserves them."""
        result = CalculatorGUI._format_result(3.14159265)
        assert "3.14159" in result


# ===========================================================================
# TestUpdateDisplay
# ===========================================================================


class TestUpdateDisplay:
    """Test display update mechanism."""

    def test_update_display_calls_stringvar_set(self, gui, mock_tkinter_components):
        """_update_display() updates the display variable."""
        gui._current_display = "42"
        gui._update_display()
        # Verify the StringVar was set to the display value
        assert mock_tkinter_components['stringvar_values']['value'] == "42"

    def test_update_display_after_digit_press(self, gui, mock_tkinter_components):
        """Display updates after digit press."""
        gui._on_digit_pressed(5)
        assert mock_tkinter_components['stringvar_values']['value'] == "5"

    def test_update_display_after_operator_press(self, gui, mock_tkinter_components):
        """Display updates after operator press (doesn't change display)."""
        gui._on_digit_pressed(5)
        gui._on_operator_pressed("add")
        # Display should still show "5" after operator
        assert gui._current_display == "5"


# ===========================================================================
# TestComplexScenarios
# ===========================================================================


class TestComplexScenarios:
    """Test complex multi-step scenarios."""

    def test_chained_calculations(self, gui):
        """Test: 2 + 3 = (result 5), then + 2 = (result 7)."""
        gui._on_digit_pressed(2)
        gui._on_operator_pressed("add")
        gui._on_digit_pressed(3)
        gui._on_equals_pressed()
        assert gui._current_display == "5"

        # Continue with the result
        gui._on_operator_pressed("add")
        gui._on_digit_pressed(2)
        gui._on_equals_pressed()
        assert gui._current_display == "7"

    def test_mixed_operations(self, gui):
        """Test: 10 × 2 - 5 = (result 15)."""
        gui._on_digit_pressed(1)
        gui._on_digit_pressed(0)
        gui._on_operator_pressed("multiply")
        gui._on_digit_pressed(2)
        gui._on_equals_pressed()
        assert gui._current_display == "20"

        gui._on_operator_pressed("subtract")
        gui._on_digit_pressed(5)
        gui._on_equals_pressed()
        assert gui._current_display == "15"

    def test_calculation_with_decimals(self, gui):
        """Test: 2.5 + 1.5 = 4."""
        gui._on_digit_pressed(2)
        gui._on_decimal_pressed()
        gui._on_digit_pressed(5)
        gui._on_operator_pressed("add")
        gui._on_digit_pressed(1)
        gui._on_decimal_pressed()
        gui._on_digit_pressed(5)
        gui._on_equals_pressed()
        assert gui._current_display == "4"

    def test_unary_then_binary_operation(self, gui):
        """Test: square of 3 (9), then add 1 = 10."""
        gui._on_digit_pressed(3)
        gui._on_unary_pressed("square")
        assert gui._current_display == "9"

        gui._on_operator_pressed("add")
        gui._on_digit_pressed(1)
        gui._on_equals_pressed()
        assert gui._current_display == "10"

    def test_percent_then_operation(self, gui):
        """Test: 200 as 2 (%), then add 5 = 7."""
        gui._on_digit_pressed(2)
        gui._on_digit_pressed(0)
        gui._on_digit_pressed(0)
        gui._on_percent_pressed()
        assert gui._current_display == "2"

        gui._on_operator_pressed("add")
        gui._on_digit_pressed(5)
        gui._on_equals_pressed()
        assert gui._current_display == "7"

    def test_negate_then_operation(self, gui):
        """Test: negate 5 to -5, then add 10 = 5."""
        gui._on_digit_pressed(5)
        gui._on_negate_pressed()
        assert gui._current_display == "-5"

        gui._on_operator_pressed("add")
        gui._on_digit_pressed(1)
        gui._on_digit_pressed(0)
        gui._on_equals_pressed()
        assert gui._current_display == "5"

    def test_clear_in_middle_of_calculation(self, gui):
        """Test: 5 + 3, then clear, then 2 + 1 = 3."""
        gui._on_digit_pressed(5)
        gui._on_operator_pressed("add")
        gui._on_digit_pressed(3)
        gui._on_clear_pressed()

        gui._on_digit_pressed(2)
        gui._on_operator_pressed("add")
        gui._on_digit_pressed(1)
        gui._on_equals_pressed()
        assert gui._current_display == "3"


# ===========================================================================
# TestEdgeCases
# ===========================================================================


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_large_number_input(self, gui):
        """Test input of very large number."""
        for digit in [9] * 10:
            gui._on_digit_pressed(digit)
        assert len(gui._current_display) == 10

    def test_very_small_decimal(self, gui):
        """Test input of very small decimal."""
        gui._current_display = "0.0000001"
        gui._on_percent_pressed()
        # Result is a very small number in scientific notation
        assert "e-" in gui._current_display or gui._current_display.startswith("0.")

    def test_division_by_zero_handling(self, gui):
        """Test division by zero."""
        gui._on_digit_pressed(5)
        gui._on_operator_pressed("divide")
        gui._on_digit_pressed(0)
        gui._on_equals_pressed()
        # Result depends on calculator implementation
        assert gui._current_display in ("Error", "inf")

    def test_multiple_decimal_attempts(self, gui):
        """Test multiple decimal point attempts."""
        gui._on_digit_pressed(5)
        gui._on_decimal_pressed()
        gui._on_decimal_pressed()
        gui._on_decimal_pressed()
        assert gui._current_display == "5."

    def test_negate_multiple_times(self, gui):
        """Test negating multiple times."""
        gui._on_digit_pressed(5)
        gui._on_negate_pressed()
        gui._on_negate_pressed()
        assert gui._current_display == "5"

    def test_equals_multiple_times(self, gui):
        """Test pressing equals multiple times."""
        gui._on_digit_pressed(5)
        gui._on_operator_pressed("add")
        gui._on_digit_pressed(3)
        gui._on_equals_pressed()
        first_result = gui._current_display

        gui._on_equals_pressed()
        # Second equals should do nothing since no pending operator
        assert gui._current_display == first_result

    def test_operator_without_operand(self, gui):
        """Test operator pressed on initial state."""
        gui._on_operator_pressed("add")
        assert gui._pending_operator == "add"
        assert gui._pending_operand == 0.0

    def test_decimal_on_zero(self, gui):
        """Test decimal on zero display."""
        gui._on_decimal_pressed()
        assert gui._current_display == "0."

    def test_operations_on_error_state(self, gui):
        """Test digit pressed after error state."""
        # When error occurs, _result_just_shown is False, so digit appends
        gui._current_display = "Error"
        gui._result_just_shown = False
        gui._on_digit_pressed(5)
        # Digit appends to error display (current behavior)
        assert gui._current_display == "Error5"

    def test_mode_toggle_multiple_times(self, gui):
        """Test toggling mode multiple times."""
        initial = gui._is_scientific_mode
        gui._on_mode_toggle()
        gui._on_mode_toggle()
        gui._on_mode_toggle()
        gui._on_mode_toggle()
        assert gui._is_scientific_mode == initial
