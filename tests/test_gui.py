"""Test suite for the Tkinter calculator GUI.

Tests the CalculatorGUI class, including widget initialization, display updates,
number input, arithmetic operations, error handling, and scientific mode.
"""

import tkinter as tk
import pytest
from unittest.mock import MagicMock, patch, call

from src.presentation.gui import CalculatorGUI
from src.logic import Calculator


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def root():
    """Create a hidden tkinter root window for testing.

    Yields:
        A tk.Tk instance with withdraw() called to hide the window.
    """
    r = tk.Tk()
    r.withdraw()
    yield r
    r.destroy()


@pytest.fixture
def gui(root):
    """Create a CalculatorGUI instance for testing.

    Yields:
        A CalculatorGUI instance tied to the test root window.
    """
    return CalculatorGUI(root)


# ============================================================================
# GUI INITIALIZATION TESTS
# ============================================================================

class TestGUIInitialization:
    """Test suite for GUI initialization and widget creation."""

    def test_gui_initializes_without_error(self, root):
        """Test that GUI initializes without raising an exception."""
        gui = CalculatorGUI(root)
        assert gui is not None

    def test_gui_creates_display_label(self, gui):
        """Test that the display label widget is created."""
        assert hasattr(gui, "_display_label")
        assert isinstance(gui._display_label, tk.Label)

    def test_gui_creates_display_var(self, gui):
        """Test that the display StringVar is created."""
        assert hasattr(gui, "_display_var")
        assert isinstance(gui._display_var, tk.StringVar)

    def test_gui_display_initial_value(self, gui):
        """Test that the display initially shows '0'."""
        assert gui._display_var.get() == "0"

    def test_gui_creates_toggle_button(self, gui):
        """Test that the scientific mode toggle button is created."""
        assert hasattr(gui, "_toggle_btn")
        assert isinstance(gui._toggle_btn, tk.Button)

    def test_gui_creates_button_frame(self, gui):
        """Test that the main button frame is created."""
        assert hasattr(gui, "_btn_frame")
        assert isinstance(gui._btn_frame, tk.Frame)

    def test_gui_creates_scientific_frame(self, gui):
        """Test that the scientific operations frame is created."""
        assert hasattr(gui, "_sci_frame")
        assert isinstance(gui._sci_frame, tk.Frame)

    def test_gui_initializes_state_variables(self, gui):
        """Test that all state variables are properly initialized."""
        assert gui._first_operand is None
        assert gui._pending_op is None
        assert gui._reset_on_next_digit is False
        assert gui._scientific_visible is False

    def test_gui_creates_calculator_instance(self, gui):
        """Test that the GUI creates its own Calculator instance."""
        assert hasattr(gui, "_calc")
        assert isinstance(gui._calc, Calculator)

    def test_gui_window_title_is_set(self, root, gui):
        """Test that the root window title is set to 'Calculator'."""
        assert root.title() == "Calculator"

    def test_gui_window_not_resizable(self, root, gui):
        """Test that the root window is set as non-resizable."""
        # Check geometry configuration
        root.update()
        assert root.resizable() == (False, False)


# ============================================================================
# DISPLAY UPDATE TESTS
# ============================================================================

class TestDisplayUpdate:
    """Test suite for display update methods."""

    def test_update_display_sets_value(self, gui):
        """Test that _update_display() sets the display text."""
        gui._update_display("123")
        assert gui._current_display() == "123"

    def test_current_display_returns_display_text(self, gui):
        """Test that _current_display() returns the current display value."""
        gui._display_var.set("456")
        assert gui._current_display() == "456"

    def test_update_display_replaces_previous_value(self, gui):
        """Test that _update_display() replaces the previous value."""
        gui._update_display("123")
        gui._update_display("456")
        assert gui._current_display() == "456"

    def test_update_display_with_error_message(self, gui):
        """Test that _update_display() can show error messages."""
        gui._update_display("Error: Division by zero")
        assert gui._current_display() == "Error: Division by zero"

    def test_update_display_with_empty_string(self, gui):
        """Test that _update_display() handles empty strings."""
        gui._update_display("")
        assert gui._current_display() == ""

    def test_update_display_with_large_number(self, gui):
        """Test that _update_display() handles large numbers."""
        large_num = "9" * 50
        gui._update_display(large_num)
        assert gui._current_display() == large_num

    def test_update_display_with_special_characters(self, gui):
        """Test that _update_display() handles special characters in display."""
        gui._update_display("Error: Invalid input!")
        assert gui._current_display() == "Error: Invalid input!"

    def test_parse_display_returns_float(self, gui):
        """Test that _parse_display() returns a float value."""
        gui._update_display("42.5")
        result = gui._parse_display()
        assert result == 42.5
        assert isinstance(result, float)

    def test_parse_display_with_integer_string(self, gui):
        """Test that _parse_display() converts integer strings to float."""
        gui._update_display("42")
        result = gui._parse_display()
        assert result == 42.0

    def test_parse_display_with_negative_number(self, gui):
        """Test that _parse_display() handles negative numbers."""
        gui._update_display("-123.45")
        result = gui._parse_display()
        assert result == -123.45

    def test_parse_display_raises_valueerror_on_invalid_input(self, gui):
        """Test that _parse_display() raises ValueError on non-numeric input."""
        gui._update_display("Error: invalid")
        with pytest.raises(ValueError):
            gui._parse_display()

    def test_parse_display_with_zero(self, gui):
        """Test that _parse_display() handles zero."""
        gui._update_display("0")
        result = gui._parse_display()
        assert result == 0.0


# ============================================================================
# NUMBER INPUT TESTS
# ============================================================================

class TestNumberInput:
    """Test suite for number input handling."""

    def test_on_number_click_single_digit(self, gui):
        """Test that a single digit is displayed when clicked."""
        gui._on_number_click("5")
        assert gui._current_display() == "5"

    def test_on_number_click_appends_digit(self, gui):
        """Test that subsequent digits are appended."""
        gui._on_number_click("1")
        gui._on_number_click("2")
        gui._on_number_click("3")
        assert gui._current_display() == "123"

    def test_on_number_click_leading_zero_replaced(self, gui):
        """Test that leading zero is replaced by first digit."""
        gui._on_number_click("5")
        assert gui._current_display() == "5"

    def test_on_number_click_zero_after_non_zero(self, gui):
        """Test that zero is appended after non-zero digits."""
        gui._on_number_click("5")
        gui._on_number_click("0")
        assert gui._current_display() == "50"

    def test_on_number_click_decimal_point(self, gui):
        """Test that a decimal point is appended correctly."""
        gui._on_number_click("5")
        gui._on_number_click(".")
        gui._on_number_click("3")
        assert gui._current_display() == "5.3"

    def test_on_number_click_duplicate_decimal_rejected(self, gui):
        """Test that duplicate decimal points are rejected."""
        gui._on_number_click("5")
        gui._on_number_click(".")
        gui._on_number_click("3")
        gui._on_number_click(".")
        # Second decimal should not be added
        assert gui._current_display() == "5.3"

    def test_on_number_click_decimal_as_first_input(self, gui):
        """Test that a decimal point can be the first input."""
        gui._on_number_click(".")
        assert gui._current_display() == "0."

    def test_on_number_click_after_reset_flag_set(self, gui):
        """Test that a digit after reset flag replaces the display."""
        gui._update_display("42")
        gui._reset_on_next_digit = True
        gui._on_number_click("7")
        assert gui._current_display() == "7"
        assert gui._reset_on_next_digit is False

    def test_on_number_click_all_digits_0_9(self, gui):
        """Test that all digits 0-9 can be input."""
        for digit in "0123456789":
            gui._on_number_click("C")  # Clear between digits
            gui._on_clear_click()
            gui._on_number_click(digit)
            assert gui._current_display() == digit

    def test_on_number_click_large_number(self, gui):
        """Test that a large number can be input."""
        for _ in range(20):
            gui._on_number_click("9")
        assert len(gui._current_display()) == 20

    def test_on_number_click_resets_flag_on_append(self, gui):
        """Test that reset flag is cleared when appending to existing number."""
        gui._update_display("5")
        gui._reset_on_next_digit = True
        gui._on_number_click(".")
        # After decimal, if we add digit, reset should be cleared
        gui._on_number_click("3")
        assert gui._reset_on_next_digit is False

    def test_on_number_click_zero_and_decimal(self, gui):
        """Test that entering '0.' works correctly."""
        gui._on_number_click("0")
        gui._on_number_click(".")
        assert gui._current_display() == "0."

    def test_on_number_click_multiple_decimals_in_chain(self, gui):
        """Test that multiple decimal point attempts are all rejected."""
        gui._on_number_click("1")
        gui._on_number_click(".")
        gui._on_number_click("2")
        gui._on_number_click(".")
        gui._on_number_click(".")
        gui._on_number_click("3")
        assert gui._current_display() == "1.23"


# ============================================================================
# ARITHMETIC OPERATION TESTS
# ============================================================================

class TestArithmeticOperations:
    """Test suite for arithmetic operations."""

    def test_on_operation_click_basic_add(self, gui):
        """Test that addition operation is recorded."""
        gui._on_number_click("5")
        gui._on_operation_click("+")
        assert gui._pending_op == "+"
        assert gui._first_operand == 5.0
        assert gui._reset_on_next_digit is True

    def test_on_operation_click_basic_subtract(self, gui):
        """Test that subtraction operation is recorded."""
        gui._on_number_click("5")
        gui._on_operation_click("-")
        assert gui._pending_op == "-"
        assert gui._first_operand == 5.0

    def test_on_operation_click_basic_multiply(self, gui):
        """Test that multiplication operation is recorded."""
        gui._on_number_click("5")
        gui._on_operation_click("*")
        assert gui._pending_op == "*"
        assert gui._first_operand == 5.0

    def test_on_operation_click_basic_divide(self, gui):
        """Test that division operation is recorded."""
        gui._on_number_click("5")
        gui._on_operation_click("/")
        assert gui._pending_op == "/"
        assert gui._first_operand == 5.0

    def test_on_operation_click_basic_power(self, gui):
        """Test that power operation is recorded."""
        gui._on_number_click("5")
        gui._on_operation_click("^")
        assert gui._pending_op == "^"
        assert gui._first_operand == 5.0

    def test_on_equals_click_simple_addition(self, gui):
        """Test simple addition: 5 + 3."""
        gui._on_number_click("5")
        gui._on_operation_click("+")
        gui._on_number_click("3")
        gui._on_equals_click()
        assert gui._current_display() == "8"

    def test_on_equals_click_simple_subtraction(self, gui):
        """Test simple subtraction: 10 - 3."""
        gui._on_number_click("1")
        gui._on_number_click("0")
        gui._on_operation_click("-")
        gui._on_number_click("3")
        gui._on_equals_click()
        assert gui._current_display() == "7"

    def test_on_equals_click_simple_multiplication(self, gui):
        """Test simple multiplication: 4 * 5."""
        gui._on_number_click("4")
        gui._on_operation_click("*")
        gui._on_number_click("5")
        gui._on_equals_click()
        assert gui._current_display() == "20"

    def test_on_equals_click_simple_division(self, gui):
        """Test simple division: 20 / 4."""
        gui._on_number_click("2")
        gui._on_number_click("0")
        gui._on_operation_click("/")
        gui._on_number_click("4")
        gui._on_equals_click()
        assert gui._current_display() == "5"

    def test_on_equals_click_simple_power(self, gui):
        """Test power operation: 2 ^ 3."""
        gui._on_number_click("2")
        gui._on_operation_click("^")
        gui._on_number_click("3")
        gui._on_equals_click()
        assert gui._current_display() == "8"

    def test_on_equals_click_division_by_zero_displays_error(self, gui):
        """Test that division by zero displays an error message."""
        gui._on_number_click("5")
        gui._on_operation_click("/")
        gui._on_number_click("0")
        gui._on_equals_click()
        assert "Error" in gui._current_display()

    def test_on_equals_click_no_pending_op_is_noop(self, gui):
        """Test that equals without a pending operation is a no-op."""
        gui._update_display("42")
        gui._on_equals_click()
        assert gui._current_display() == "42"

    def test_on_operation_click_chains_operations_left_to_right(self, gui):
        """Test chained operations: 3 + 4 * resolves first."""
        gui._on_number_click("3")
        gui._on_operation_click("+")
        gui._on_number_click("4")
        gui._on_operation_click("*")
        # After second operation, first should be resolved: 3 + 4 = 7
        assert gui._current_display() == "7"
        assert gui._pending_op == "*"

    def test_on_operation_click_with_floating_point(self, gui):
        """Test operations with floating point numbers."""
        gui._on_number_click("5")
        gui._on_number_click(".")
        gui._on_number_click("5")
        gui._on_operation_click("+")
        gui._on_number_click("3")
        gui._on_number_click(".")
        gui._on_number_click("2")
        gui._on_equals_click()
        # 5.5 + 3.2 = 8.7
        result = float(gui._current_display())
        assert abs(result - 8.7) < 0.0001

    def test_on_operation_click_with_negative_numbers(self, gui):
        """Test operations with negative first operand."""
        gui._on_number_click("5")
        gui._on_negate_click()
        gui._on_operation_click("+")
        gui._on_number_click("3")
        gui._on_equals_click()
        assert gui._current_display() == "-2"

    def test_on_operation_click_with_zero_operand(self, gui):
        """Test that operation with zero works correctly."""
        gui._on_operation_click("+")
        gui._on_number_click("5")
        gui._on_equals_click()
        assert gui._current_display() == "5"

    def test_on_operation_click_clears_state_after_equals(self, gui):
        """Test that state is cleared after equals."""
        gui._on_number_click("5")
        gui._on_operation_click("+")
        gui._on_number_click("3")
        gui._on_equals_click()
        assert gui._pending_op is None
        assert gui._first_operand is None

    def test_execute_operation_with_invalid_display_shows_error(self, gui):
        """Test that invalid display during operation shows error."""
        gui._first_operand = 5.0
        gui._pending_op = "+"
        gui._update_display("Error: something")
        gui._execute_operation()
        assert "Error" in gui._current_display()

    def test_on_operation_click_with_error_display_clears(self, gui):
        """Test that clicking operation with error display clears it."""
        gui._update_display("Error: something")
        gui._on_operation_click("+")
        assert gui._current_display() == "0"

    def test_chained_operations_three_operations_in_sequence(self, gui):
        """Test three chained operations: 2 + 3 * 4 - 1."""
        gui._on_number_click("2")
        gui._on_operation_click("+")
        gui._on_number_click("3")
        gui._on_operation_click("*")
        # 2 + 3 = 5
        assert gui._current_display() == "5"
        gui._on_number_click("4")
        gui._on_operation_click("-")
        # 5 * 4 = 20
        assert gui._current_display() == "20"
        gui._on_number_click("1")
        gui._on_equals_click()
        # 20 - 1 = 19
        assert gui._current_display() == "19"


# ============================================================================
# CLEAR AND BACKSPACE TESTS
# ============================================================================

class TestClearAndBackspace:
    """Test suite for clear and backspace operations."""

    def test_on_clear_click_resets_display_to_zero(self, gui):
        """Test that clear button sets display to '0'."""
        gui._update_display("123")
        gui._on_clear_click()
        assert gui._current_display() == "0"

    def test_on_clear_click_clears_pending_operation(self, gui):
        """Test that clear resets pending operation state."""
        gui._on_number_click("5")
        gui._on_operation_click("+")
        gui._on_clear_click()
        assert gui._pending_op is None
        assert gui._first_operand is None

    def test_on_clear_click_resets_reset_flag(self, gui):
        """Test that clear resets the reset_on_next_digit flag."""
        gui._reset_on_next_digit = True
        gui._on_clear_click()
        assert gui._reset_on_next_digit is False

    def test_on_backspace_click_removes_last_character(self, gui):
        """Test that backspace removes the last character."""
        gui._on_number_click("1")
        gui._on_number_click("2")
        gui._on_number_click("3")
        gui._on_backspace_click()
        assert gui._current_display() == "12"

    def test_on_backspace_click_on_single_digit_shows_zero(self, gui):
        """Test that backspace on single digit shows '0'."""
        gui._on_number_click("5")
        gui._on_backspace_click()
        assert gui._current_display() == "0"

    def test_on_backspace_click_on_zero_stays_zero(self, gui):
        """Test that backspace on '0' remains '0'."""
        gui._on_backspace_click()
        assert gui._current_display() == "0"

    def test_on_backspace_click_on_decimal(self, gui):
        """Test that backspace removes decimal point."""
        gui._on_number_click("5")
        gui._on_number_click(".")
        gui._on_backspace_click()
        assert gui._current_display() == "5"

    def test_on_backspace_click_on_negative_sign_shows_zero(self, gui):
        """Test that backspace on just '-' shows '0'."""
        gui._update_display("-")
        gui._on_backspace_click()
        assert gui._current_display() == "0"

    def test_on_backspace_click_on_error_message(self, gui):
        """Test that backspace on error message clears to '0'."""
        gui._update_display("Error: Division by zero")
        gui._on_backspace_click()
        assert gui._current_display() == "0"

    def test_on_backspace_click_on_error_resets_state(self, gui):
        """Test that backspace on error resets pending operation state."""
        gui._update_display("Error: something")
        gui._first_operand = 5.0
        gui._pending_op = "+"
        gui._on_backspace_click()
        assert gui._pending_op is None
        assert gui._first_operand is None

    def test_on_backspace_click_multiple_times(self, gui):
        """Test multiple consecutive backspaces."""
        gui._on_number_click("1")
        gui._on_number_click("2")
        gui._on_number_click("3")
        gui._on_backspace_click()
        gui._on_backspace_click()
        gui._on_backspace_click()
        assert gui._current_display() == "0"

    def test_on_backspace_click_on_decimal_number(self, gui):
        """Test backspace on decimal number."""
        gui._on_number_click("3")
        gui._on_number_click(".")
        gui._on_number_click("1")
        gui._on_number_click("4")
        gui._on_backspace_click()
        assert gui._current_display() == "3.1"

    def test_on_backspace_click_after_calculation(self, gui):
        """Test backspace after a calculation result."""
        gui._on_number_click("5")
        gui._on_operation_click("+")
        gui._on_number_click("3")
        gui._on_equals_click()
        gui._on_backspace_click()
        assert gui._current_display() == "0"


# ============================================================================
# NEGATE AND PERCENT TESTS
# ============================================================================

class TestNegateAndPercent:
    """Test suite for negation and percent operations."""

    def test_on_negate_click_positive_becomes_negative(self, gui):
        """Test that negating a positive number makes it negative."""
        gui._on_number_click("5")
        gui._on_negate_click()
        assert gui._current_display() == "-5"

    def test_on_negate_click_negative_becomes_positive(self, gui):
        """Test that negating a negative number makes it positive."""
        gui._on_number_click("5")
        gui._on_negate_click()
        gui._on_negate_click()
        assert gui._current_display() == "5"

    def test_on_negate_click_zero_remains_zero(self, gui):
        """Test that negating zero remains zero."""
        gui._on_negate_click()
        assert gui._current_display() == "0"

    def test_on_negate_click_on_float(self, gui):
        """Test that negating a float works correctly."""
        gui._on_number_click("5")
        gui._on_number_click(".")
        gui._on_number_click("5")
        gui._on_negate_click()
        assert gui._current_display() == "-5.5"

    def test_on_negate_click_on_error_is_noop(self, gui):
        """Test that negating an error message does nothing."""
        gui._update_display("Error: something")
        gui._on_negate_click()
        assert gui._current_display() == "Error: something"

    def test_on_negate_click_double_negate(self, gui):
        """Test that double negation returns to original."""
        gui._on_number_click("7")
        gui._on_negate_click()
        gui._on_negate_click()
        assert gui._current_display() == "7"

    def test_on_percent_click_divides_by_100(self, gui):
        """Test that percent divides the value by 100."""
        gui._on_number_click("5")
        gui._on_number_click("0")
        gui._on_percent_click()
        assert gui._current_display() == "0.5"

    def test_on_percent_click_on_one(self, gui):
        """Test that percent of 1 is 0.01."""
        gui._on_number_click("1")
        gui._on_percent_click()
        assert gui._current_display() == "0.01"

    def test_on_percent_click_on_zero(self, gui):
        """Test that percent of zero is zero."""
        gui._on_percent_click()
        assert gui._current_display() == "0"

    def test_on_percent_click_on_negative_number(self, gui):
        """Test that percent of negative number is negative."""
        gui._on_number_click("5")
        gui._on_negate_click()
        gui._on_percent_click()
        assert gui._current_display() == "-0.05"

    def test_on_percent_click_on_error_is_noop(self, gui):
        """Test that percent on error message does nothing."""
        gui._update_display("Error: something")
        gui._on_percent_click()
        assert gui._current_display() == "Error: something"

    def test_on_percent_click_on_float(self, gui):
        """Test that percent works on float values."""
        gui._on_number_click("2")
        gui._on_number_click("5")
        gui._on_number_click(".")
        gui._on_number_click("5")
        gui._on_percent_click()
        # 25.5 / 100 = 0.255
        result = float(gui._current_display())
        assert abs(result - 0.255) < 0.0001

    def test_negate_then_percent(self, gui):
        """Test negating then taking percent."""
        gui._on_number_click("1")
        gui._on_number_click("0")
        gui._on_negate_click()
        gui._on_percent_click()
        assert gui._current_display() == "-0.1"

    def test_percent_then_negate(self, gui):
        """Test taking percent then negating."""
        gui._on_number_click("5")
        gui._on_percent_click()
        gui._on_negate_click()
        assert gui._current_display() == "-0.05"


# ============================================================================
# SCIENTIFIC MODE TESTS
# ============================================================================

class TestScientificMode:
    """Test suite for scientific mode toggle and operations."""

    def test_toggle_scientific_mode_shows_frame(self, gui):
        """Test that toggling scientific mode shows the frame."""
        assert gui._scientific_visible is False
        gui._toggle_scientific_mode()
        assert gui._scientific_visible is True

    def test_toggle_scientific_mode_hides_frame(self, gui):
        """Test that toggling scientific mode again hides the frame."""
        gui._toggle_scientific_mode()
        gui._toggle_scientific_mode()
        assert gui._scientific_visible is False

    def test_toggle_scientific_mode_updates_button_text_to_on(self, gui):
        """Test that toggle button text changes to 'ON' when enabled."""
        gui._toggle_scientific_mode()
        assert "ON" in gui._toggle_btn.cget("text")

    def test_toggle_scientific_mode_updates_button_text_to_off(self, gui):
        """Test that toggle button text changes to 'OFF' when disabled."""
        gui._toggle_scientific_mode()
        gui._toggle_scientific_mode()
        assert "OFF" in gui._toggle_btn.cget("text")

    def test_on_scientific_click_sqrt(self, gui):
        """Test the square root scientific operation."""
        gui._on_number_click("1")
        gui._on_number_click("6")
        gui._on_scientific_click("sqrt")
        assert gui._current_display() == "4"

    def test_on_scientific_click_square(self, gui):
        """Test the square scientific operation."""
        gui._on_number_click("5")
        gui._on_scientific_click("square")
        assert gui._current_display() == "25"

    def test_on_scientific_click_cube(self, gui):
        """Test the cube scientific operation."""
        gui._on_number_click("3")
        gui._on_scientific_click("cube")
        assert gui._current_display() == "27"

    def test_on_scientific_click_factorial(self, gui):
        """Test the factorial scientific operation."""
        gui._on_number_click("5")
        gui._on_scientific_click("factorial")
        assert gui._current_display() == "120"

    def test_on_scientific_click_sin(self, gui):
        """Test the sine scientific operation."""
        gui._on_number_click("0")
        gui._on_scientific_click("sin")
        assert gui._current_display() == "0"

    def test_on_scientific_click_cos(self, gui):
        """Test the cosine scientific operation."""
        gui._on_number_click("0")
        gui._on_scientific_click("cos")
        assert gui._current_display() == "1"

    def test_on_scientific_click_on_error_display_clears(self, gui):
        """Test that scientific op on error display clears it."""
        gui._update_display("Error: something")
        gui._on_scientific_click("sqrt")
        assert gui._current_display() == "0"

    def test_on_scientific_click_invalid_method(self, gui):
        """Test scientific op with non-existent method."""
        gui._on_number_click("5")
        gui._on_scientific_click("nonexistent_method")
        assert "Error" in gui._current_display()

    def test_on_scientific_click_sets_reset_flag(self, gui):
        """Test that scientific operation sets reset_on_next_digit flag."""
        gui._on_number_click("4")
        gui._on_scientific_click("sqrt")
        assert gui._reset_on_next_digit is True

    def test_on_scientific_click_sqrt_invalid_value_shows_error(self, gui):
        """Test that sqrt of negative number shows error."""
        gui._on_number_click("5")
        gui._on_negate_click()
        gui._on_scientific_click("sqrt")
        assert "Error" in gui._current_display()

    def test_on_scientific_click_with_float_value(self, gui):
        """Test scientific operation on float value."""
        gui._on_number_click("2")
        gui._on_number_click(".")
        gui._on_number_click("5")
        gui._on_scientific_click("square")
        # 2.5 ^ 2 = 6.25
        result = float(gui._current_display())
        assert abs(result - 6.25) < 0.0001

    def test_on_scientific_click_cube_root(self, gui):
        """Test the cube root scientific operation."""
        gui._on_number_click("2")
        gui._on_number_click("7")
        gui._on_scientific_click("cube_root")
        assert gui._current_display() == "3"

    def test_on_scientific_click_natural_log(self, gui):
        """Test the natural logarithm operation."""
        gui._on_number_click("1")
        gui._on_scientific_click("natural_log")
        assert gui._current_display() == "0"

    def test_on_scientific_click_log10(self, gui):
        """Test the base-10 logarithm operation."""
        gui._on_number_click("1")
        gui._on_number_click("0")
        gui._on_number_click("0")
        gui._on_scientific_click("log10")
        assert gui._current_display() == "2"

    def test_on_scientific_click_exp(self, gui):
        """Test the exponential operation."""
        gui._on_number_click("0")
        gui._on_scientific_click("exp")
        assert gui._current_display() == "1"

    def test_on_scientific_click_tan(self, gui):
        """Test the tangent operation."""
        gui._on_number_click("0")
        gui._on_scientific_click("tan")
        assert gui._current_display() == "0"


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

class TestErrorHandling:
    """Test suite for error handling and exception catching."""

    def test_division_by_zero_displays_error(self, gui):
        """Test that division by zero shows error message."""
        gui._on_number_click("5")
        gui._on_operation_click("/")
        gui._on_number_click("0")
        gui._on_equals_click()
        assert "Error" in gui._current_display()
        assert "Division by zero" in gui._current_display()

    def test_after_error_new_digit_clears_error(self, gui):
        """Test that entering new digit after error starts fresh."""
        gui._on_number_click("5")
        gui._on_operation_click("/")
        gui._on_number_click("0")
        gui._on_equals_click()
        gui._on_number_click("7")
        assert gui._current_display() == "7"

    def test_error_state_clears_pending_operation(self, gui):
        """Test that error state clears pending operation."""
        gui._on_number_click("5")
        gui._on_operation_click("/")
        gui._on_number_click("0")
        gui._on_equals_click()
        # After error, pending state should be cleared
        assert gui._pending_op is None
        assert gui._first_operand is None

    def test_exception_caught_and_displayed(self, gui):
        """Test that exceptions are caught and displayed as errors."""
        gui._on_number_click("5")
        gui._on_negate_click()
        # Factorial of negative number should error
        gui._on_scientific_click("factorial")
        assert "Error" in gui._current_display()

    def test_multiple_errors_in_sequence(self, gui):
        """Test that multiple errors are handled correctly."""
        gui._on_number_click("5")
        gui._on_operation_click("/")
        gui._on_number_click("0")
        gui._on_equals_click()
        assert "Error" in gui._current_display()

        gui._on_number_click("3")
        gui._on_operation_click("/")
        gui._on_number_click("0")
        gui._on_equals_click()
        assert "Error" in gui._current_display()

    def test_valueerror_displayed(self, gui):
        """Test that ValueError is caught and displayed."""
        gui._on_number_click("2")
        gui._on_negate_click()
        gui._on_scientific_click("sqrt")
        assert "Error" in gui._current_display()

    def test_format_result_with_integer_float(self, gui):
        """Test format_result strips unnecessary trailing zeros for integer floats."""
        result = CalculatorGUI._format_result(5.0)
        assert result == "5"

    def test_format_result_with_float(self, gui):
        """Test format_result keeps decimal places for non-integer floats."""
        result = CalculatorGUI._format_result(5.5)
        assert "5.5" in result

    def test_format_result_with_integer(self, gui):
        """Test format_result with integer input."""
        result = CalculatorGUI._format_result(42)
        assert result == "42"

    def test_format_result_with_very_small_number(self, gui):
        """Test format_result with very small number."""
        result = CalculatorGUI._format_result(0.0000001)
        assert "1" in result

    def test_format_result_with_trailing_zeros(self, gui):
        """Test format_result strips trailing zeros."""
        result = CalculatorGUI._format_result(1.5000)
        assert result == "1.5"


# ============================================================================
# STATE MANAGEMENT TESTS
# ============================================================================

class TestStateManagement:
    """Test suite for internal state management."""

    def test_reset_state_clears_first_operand(self, gui):
        """Test that _reset_state clears first operand."""
        gui._first_operand = 42.0
        gui._reset_state()
        assert gui._first_operand is None

    def test_reset_state_clears_pending_op(self, gui):
        """Test that _reset_state clears pending operation."""
        gui._pending_op = "+"
        gui._reset_state()
        assert gui._pending_op is None

    def test_reset_state_clears_reset_flag(self, gui):
        """Test that _reset_state clears reset_on_next_digit."""
        gui._reset_on_next_digit = True
        gui._reset_state()
        assert gui._reset_on_next_digit is False

    def test_complex_calculation_preserves_state_correctly(self, gui):
        """Test that complex calculation preserves state correctly."""
        gui._on_number_click("5")
        gui._on_operation_click("+")
        gui._on_number_click("3")
        gui._on_operation_click("*")
        # At this point: 5 + 3 = 8, pending op is *
        assert gui._pending_op == "*"
        assert gui._current_display() == "8"
        gui._on_number_click("2")
        gui._on_equals_click()
        # 8 * 2 = 16
        assert gui._current_display() == "16"
        assert gui._pending_op is None


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests for complete calculator workflows."""

    def test_full_workflow_simple_calculation(self, gui):
        """Test a complete simple calculation workflow."""
        gui._on_number_click("7")
        gui._on_operation_click("+")
        gui._on_number_click("5")
        gui._on_equals_click()
        assert gui._current_display() == "12"

    def test_full_workflow_with_backspace_correction(self, gui):
        """Test workflow with backspace correction."""
        gui._on_number_click("1")
        gui._on_number_click("2")
        gui._on_number_click("3")
        gui._on_backspace_click()
        gui._on_number_click("5")
        gui._on_operation_click("+")
        gui._on_number_click("2")
        gui._on_equals_click()
        assert gui._current_display() == "127"

    def test_full_workflow_with_clear_recovery(self, gui):
        """Test workflow with clear recovery from error."""
        gui._on_number_click("5")
        gui._on_operation_click("/")
        gui._on_number_click("0")
        gui._on_equals_click()
        gui._on_clear_click()
        gui._on_number_click("3")
        gui._on_operation_click("+")
        gui._on_number_click("2")
        gui._on_equals_click()
        assert gui._current_display() == "5"

    def test_full_workflow_scientific_operation(self, gui):
        """Test workflow with scientific operation."""
        gui._on_number_click("9")
        gui._on_scientific_click("sqrt")
        gui._on_operation_click("+")
        gui._on_number_click("1")
        gui._on_equals_click()
        assert gui._current_display() == "4"

    def test_full_workflow_multiple_chained_operations(self, gui):
        """Test multiple chained operations."""
        gui._on_number_click("1")
        gui._on_number_click("0")
        gui._on_operation_click("+")
        gui._on_number_click("5")
        gui._on_operation_click("-")
        gui._on_number_click("3")
        gui._on_operation_click("*")
        gui._on_number_click("2")
        gui._on_equals_click()
        # 10 + 5 = 15, 15 - 3 = 12, 12 * 2 = 24
        assert gui._current_display() == "24"

    def test_full_workflow_with_decimal_and_percent(self, gui):
        """Test workflow with decimal and percent."""
        gui._on_number_click("2")
        gui._on_number_click("0")
        gui._on_percent_click()
        gui._on_operation_click("+")
        gui._on_number_click("1")
        gui._on_equals_click()
        # 20 % = 0.2, 0.2 + 1 = 1.2
        result = float(gui._current_display())
        assert abs(result - 1.2) < 0.0001


# ============================================================================
# RUN METHOD TEST
# ============================================================================

class TestRunMethod:
    """Test suite for the run() method."""

    def test_run_calls_mainloop(self, root):
        """Test that run() delegates to root.mainloop()."""
        gui = CalculatorGUI(root)

        # Mock the mainloop to avoid blocking
        original_mainloop = root.mainloop
        root.mainloop = MagicMock()

        gui.run()

        # Verify mainloop was called
        root.mainloop.assert_called_once()

        # Restore original
        root.mainloop = original_mainloop
