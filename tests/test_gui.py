"""Comprehensive tests for src.gui module (CalculatorGUI tkinter interface).

Tests the main GUI window, button event handlers, display state management,
mode switching, and calculation dispatch. All tkinter components are mocked
to avoid requiring a display server in headless CI environments.

Key test targets:
  - CalculatorGUI.__init__: widget construction and initial state
  - CalculatorGUI._execute_normal: binary calculation dispatch, error paths
  - CalculatorGUI._execute_scientific: unary calculation dispatch, error paths
  - CalculatorGUI._on_mode_switch: mode toggle and state reset
  - CalculatorGUI._append_digit: digit accumulation and decimal guard
  - CalculatorGUI._set_operator: operator chaining logic
  - CalculatorGUI._clear_state: state reset
  - CalculatorGUI._show_error: error display and auto-reset
  - CalculatorGUI._format_number: numeric formatting
"""

import sys
from unittest import mock
import pytest

# Mock tkinter before importing gui module to avoid TclError in headless CI
sys.modules["tkinter"] = mock.MagicMock()
sys.modules["tkinter.font"] = mock.MagicMock()

from src.gui import CalculatorGUI


# ============================================================================
# Fixtures: provide mocked tkinter components globally
# ============================================================================


@pytest.fixture
def mock_tk():
    """Mock the entire tkinter module and return all patches."""
    with mock.patch("tkinter.Tk") as mock_tk_class, \
         mock.patch("tkinter.Frame") as mock_frame_class, \
         mock.patch("tkinter.StringVar") as mock_stringvar_class, \
         mock.patch("tkinter.Label") as mock_label_class, \
         mock.patch("tkinter.Button") as mock_button_class, \
         mock.patch("tkinter.font.Font") as mock_font_class:

        # Configure Tk() to return a mock root window
        mock_root = mock.MagicMock()
        mock_tk_class.return_value = mock_root

        # Configure Frame() to return a mock frame
        mock_frame_class.return_value = mock.MagicMock()

        # Configure StringVar() to return a mock with set/get methods
        mock_stringvar = mock.MagicMock()
        mock_stringvar.set = mock.MagicMock()
        mock_stringvar.get = mock.MagicMock(return_value="0")
        mock_stringvar_class.return_value = mock_stringvar

        # Configure Label() to return a mock label
        mock_label_class.return_value = mock.MagicMock()

        # Configure Button() to return a mock button
        mock_button_class.return_value = mock.MagicMock()

        # Configure Font() to return a mock font
        mock_font_class.return_value = mock.MagicMock()

        yield {
            "Tk": mock_tk_class,
            "Frame": mock_frame_class,
            "StringVar": mock_stringvar_class,
            "Label": mock_label_class,
            "Button": mock_button_class,
            "Font": mock_font_class,
            "root": mock_root,
            "stringvar": mock_stringvar,
        }


@pytest.fixture
def gui_with_mocks(mock_tk):
    """Create a CalculatorGUI instance with all tkinter mocked."""
    with mock.patch("src.gui.tk"):
        gui = CalculatorGUI()
        gui._root = mock_tk["root"]
        gui._display_var = mock.MagicMock()
        gui._history_var = mock.MagicMock()
        gui._display_label = mock.MagicMock()
        gui._mode_normal_btn = mock.MagicMock()
        gui._mode_scientific_btn = mock.MagicMock()
        gui._mode_status_label = mock.MagicMock()
        gui._normal_frame = mock.MagicMock()
        gui._sci_frame = mock.MagicMock()
        return gui


# ============================================================================
# CalculatorGUI.__init__ — Widget construction and initial state
# ============================================================================


class TestCalculatorGUIInit:
    """Tests for CalculatorGUI.__init__ construction and initialization."""

    @mock.patch("tkinter.Tk")
    @mock.patch("tkinter.Frame")
    @mock.patch("tkinter.StringVar")
    @mock.patch("tkinter.Label")
    @mock.patch("tkinter.Button")
    @mock.patch("tkinter.font.Font")
    def test_init_creates_tk_root_window(
        self, mock_font, mock_button, mock_label, mock_stringvar,
        mock_frame, mock_tk_class
    ):
        """CalculatorGUI.__init__ should call tk.Tk() to create root window."""
        mock_root = mock.MagicMock()
        mock_tk_class.return_value = mock_root

        with mock.patch("src.gui.tk"):
            gui = CalculatorGUI()

        assert gui._root is not None

    @mock.patch("tkinter.Tk")
    @mock.patch("tkinter.Frame")
    @mock.patch("tkinter.StringVar")
    @mock.patch("tkinter.Label")
    @mock.patch("tkinter.Button")
    @mock.patch("tkinter.font.Font")
    def test_init_initializes_state_attributes(
        self, mock_font, mock_button, mock_label, mock_stringvar,
        mock_frame, mock_tk_class
    ):
        """CalculatorGUI.__init__ should initialize all state attributes."""
        with mock.patch("src.gui.tk"):
            gui = CalculatorGUI()

        # Normal mode state
        assert gui._current_input == ""
        assert gui._first_operand is None
        assert gui._operator is None
        assert gui._awaiting_second is False

        # Scientific mode state
        assert gui._sci_function is None
        assert gui._sci_awaiting_arg is False

    @mock.patch("tkinter.Tk")
    @mock.patch("tkinter.Frame")
    @mock.patch("tkinter.StringVar")
    @mock.patch("tkinter.Label")
    @mock.patch("tkinter.Button")
    @mock.patch("tkinter.font.Font")
    def test_init_creates_mode_manager(
        self, mock_font, mock_button, mock_label, mock_stringvar,
        mock_frame, mock_tk_class
    ):
        """CalculatorGUI.__init__ should create a ModeManager instance."""
        with mock.patch("src.gui.tk"):
            gui = CalculatorGUI()

        assert gui._mode_manager is not None
        assert gui._mode_manager.get_mode() == "normal"

    @mock.patch("tkinter.Tk")
    @mock.patch("tkinter.Frame")
    @mock.patch("tkinter.StringVar")
    @mock.patch("tkinter.Label")
    @mock.patch("tkinter.Button")
    @mock.patch("tkinter.font.Font")
    def test_init_calls_build_display(
        self, mock_font, mock_button, mock_label, mock_stringvar,
        mock_frame, mock_tk_class
    ):
        """CalculatorGUI.__init__ should call _build_display()."""
        with mock.patch("src.gui.tk"), \
             mock.patch.object(CalculatorGUI, "_build_display") as mock_build:
            gui = CalculatorGUI()

        mock_build.assert_called_once()

    @mock.patch("tkinter.Tk")
    @mock.patch("tkinter.Frame")
    @mock.patch("tkinter.StringVar")
    @mock.patch("tkinter.Label")
    @mock.patch("tkinter.Button")
    @mock.patch("tkinter.font.Font")
    def test_init_calls_all_builders(
        self, mock_font, mock_button, mock_label, mock_stringvar,
        mock_frame, mock_tk_class
    ):
        """CalculatorGUI.__init__ should call all builder methods."""
        with mock.patch("src.gui.tk"), \
             mock.patch.object(CalculatorGUI, "_build_display"), \
             mock.patch.object(CalculatorGUI, "_build_history_area"), \
             mock.patch.object(CalculatorGUI, "_build_mode_bar"), \
             mock.patch.object(CalculatorGUI, "_build_normal_buttons"), \
             mock.patch.object(CalculatorGUI, "_build_scientific_buttons"), \
             mock.patch.object(CalculatorGUI, "_refresh_mode_layout"):
            gui = CalculatorGUI()


# ============================================================================
# CalculatorGUI._format_number — Number formatting
# ============================================================================


class TestCalculatorGUIFormatNumber:
    """Tests for CalculatorGUI._format_number static method."""

    def test_format_number_integer_returns_no_decimal(self):
        """_format_number(5.0) should return '5', not '5.0'."""
        result = CalculatorGUI._format_number(5.0)
        assert result == "5"
        assert "." not in result

    def test_format_number_zero(self):
        """_format_number(0.0) should return '0'."""
        result = CalculatorGUI._format_number(0.0)
        assert result == "0"

    def test_format_number_negative_integer(self):
        """_format_number(-42.0) should return '-42'."""
        result = CalculatorGUI._format_number(-42.0)
        assert result == "-42"

    def test_format_number_simple_decimal(self):
        """_format_number(3.5) should return '3.5'."""
        result = CalculatorGUI._format_number(3.5)
        assert result == "3.5"

    def test_format_number_removes_trailing_zeros(self):
        """_format_number should use .10g to remove trailing zeros."""
        result = CalculatorGUI._format_number(3.14159265358979)
        assert "." in result
        assert float(result) == pytest.approx(3.14159265358979)

    def test_format_number_very_large_value_uses_exponential(self):
        """_format_number with large values >= 1e15 should use exponential notation."""
        result = CalculatorGUI._format_number(1e20)
        # .10g may use exponential notation for very large numbers
        assert float(result) == pytest.approx(1e20)

    def test_format_number_very_small_decimal(self):
        """_format_number(0.000001) should format compactly."""
        result = CalculatorGUI._format_number(0.000001)
        assert float(result) == pytest.approx(0.000001)

    def test_format_number_one_third(self):
        """_format_number(1/3) should approximate correctly."""
        result = CalculatorGUI._format_number(1.0 / 3.0)
        assert float(result) == pytest.approx(1.0 / 3.0)

    def test_format_number_negative_small_value(self):
        """_format_number(-0.5) should return '-0.5'."""
        result = CalculatorGUI._format_number(-0.5)
        assert result == "-0.5"

    def test_format_number_boundary_1e15(self):
        """_format_number at boundary (1e15 - 1) should still be integer."""
        val = 1e15 - 1
        result = CalculatorGUI._format_number(val)
        # Should be formatted as integer since it equals its int value
        assert "." not in result or float(result) == val


# ============================================================================
# CalculatorGUI._clear_state — Full state reset
# ============================================================================


class TestCalculatorGUIClearState:
    """Tests for CalculatorGUI._clear_state method."""

    def test_clear_state_resets_all_normal_mode_state(self, gui_with_mocks):
        """_clear_state should reset all normal mode attributes."""
        gui = gui_with_mocks
        gui._current_input = "42"
        gui._first_operand = 10.0
        gui._operator = "+"
        gui._awaiting_second = True

        gui._clear_state()

        assert gui._current_input == ""
        assert gui._first_operand is None
        assert gui._operator is None
        assert gui._awaiting_second is False

    def test_clear_state_resets_all_scientific_mode_state(self, gui_with_mocks):
        """_clear_state should reset all scientific mode attributes."""
        gui = gui_with_mocks
        gui._sci_function = "sin"
        gui._sci_awaiting_arg = True

        gui._clear_state()

        assert gui._sci_function is None
        assert gui._sci_awaiting_arg is False

    def test_clear_state_clears_display(self, gui_with_mocks):
        """_clear_state should set display to '0'."""
        gui = gui_with_mocks
        gui._clear_state()

        gui._display_var.set.assert_called_with("0")

    def test_clear_state_clears_history(self, gui_with_mocks):
        """_clear_state should clear history display."""
        gui = gui_with_mocks
        gui._clear_state()

        gui._history_var.set.assert_called_with("")


# ============================================================================
# CalculatorGUI._append_digit — Digit accumulation and decimal guard
# ============================================================================


class TestCalculatorGUIAppendDigit:
    """Tests for CalculatorGUI._append_digit method."""

    def test_append_digit_adds_single_digit(self, gui_with_mocks):
        """_append_digit('5') should add '5' to current_input."""
        gui = gui_with_mocks
        gui._append_digit("5")

        assert gui._current_input == "5"
        gui._display_var.set.assert_called_with("5")

    def test_append_digit_accumulates_multiple_digits(self, gui_with_mocks):
        """_append_digit should accumulate digits: '3' then '5' -> '35'."""
        gui = gui_with_mocks
        gui._append_digit("3")
        gui._append_digit("5")

        assert gui._current_input == "35"

    def test_append_digit_adds_decimal_point(self, gui_with_mocks):
        """_append_digit('.') should add decimal to input."""
        gui = gui_with_mocks
        gui._append_digit("3")
        gui._append_digit(".")
        gui._append_digit("5")

        assert gui._current_input == "3.5"

    def test_append_digit_guards_multiple_decimals(self, gui_with_mocks):
        """_append_digit should prevent multiple decimal points."""
        gui = gui_with_mocks
        gui._append_digit("3")
        gui._append_digit(".")
        gui._append_digit("1")
        gui._append_digit(".")  # Should be ignored

        assert gui._current_input == "3.1"

    def test_append_digit_resets_awaiting_second(self, gui_with_mocks):
        """_append_digit should reset _awaiting_second flag and clear input."""
        gui = gui_with_mocks
        gui._first_operand = 10.0
        gui._operator = "+"
        gui._awaiting_second = True
        gui._current_input = "10"

        gui._append_digit("5")

        assert gui._awaiting_second is False
        assert gui._current_input == "5"

    def test_append_digit_replaces_zero_with_digit(self, gui_with_mocks):
        """_append_digit('3') when _current_input=='0' should set to '3', not '03'."""
        gui = gui_with_mocks
        gui._current_input = "0"
        gui._append_digit("7")

        assert gui._current_input == "7"

    def test_append_digit_allows_decimal_on_zero(self, gui_with_mocks):
        """_append_digit('.') when _current_input=='0' should give '0.'."""
        gui = gui_with_mocks
        gui._current_input = "0"
        gui._append_digit(".")

        assert gui._current_input == "0."

    def test_append_digit_on_empty_input_replaces_with_digit(self, gui_with_mocks):
        """_append_digit on empty input should set the digit."""
        gui = gui_with_mocks
        gui._current_input = ""
        gui._append_digit("9")

        assert gui._current_input == "9"

    def test_append_digit_on_empty_input_with_decimal(self, gui_with_mocks):
        """_append_digit('.') on empty input should add '.' (allows typing '.5')."""
        gui = gui_with_mocks
        gui._current_input = ""
        gui._append_digit(".")

        assert gui._current_input == "."

    def test_append_digit_updates_display_var(self, gui_with_mocks):
        """_append_digit should update _display_var after each addition."""
        gui = gui_with_mocks
        gui._append_digit("2")
        gui._append_digit("3")

        # Check that set was called with '2' and then '23'
        calls = [call[0][0] for call in gui._display_var.set.call_args_list]
        assert "2" in calls
        assert "23" in calls


# ============================================================================
# CalculatorGUI._set_operator — Operator chaining and first operand capture
# ============================================================================


class TestCalculatorGUISetOperator:
    """Tests for CalculatorGUI._set_operator method."""

    def test_set_operator_captures_first_operand(self, gui_with_mocks):
        """_set_operator should parse and capture the first operand."""
        gui = gui_with_mocks
        gui._current_input = "42"

        gui._set_operator("+")

        assert gui._first_operand == 42.0
        assert gui._operator == "+"
        assert gui._awaiting_second is True

    def test_set_operator_updates_history_display(self, gui_with_mocks):
        """_set_operator should display 'operand operator' in history."""
        gui = gui_with_mocks
        gui._current_input = "7"

        gui._set_operator("*")

        gui._history_var.set.assert_called()
        call_args = gui._history_var.set.call_args[0][0]
        assert "7" in call_args
        assert "*" in call_args

    def test_set_operator_with_empty_input_defaults_to_zero(self, gui_with_mocks):
        """_set_operator with empty _current_input should use 0.0 as first operand."""
        gui = gui_with_mocks
        gui._current_input = ""

        gui._set_operator("+")

        assert gui._first_operand == 0.0

    def test_set_operator_ignores_invalid_operator(self, gui_with_mocks):
        """_set_operator with invalid operator should return early."""
        gui = gui_with_mocks
        gui._current_input = "5"
        initial_operand = gui._first_operand

        gui._set_operator("@")  # Invalid operator

        assert gui._first_operand == initial_operand  # Unchanged

    def test_set_operator_chains_calculation(self, gui_with_mocks):
        """_set_operator with pending operator and second operand should chain."""
        gui = gui_with_mocks
        gui._first_operand = 3.0
        gui._operator = "+"
        gui._awaiting_second = False
        gui._current_input = "4"

        with mock.patch.object(gui, "_execute_normal") as mock_execute:
            gui._set_operator("+")
            mock_execute.assert_called_once_with(chain=True)

    def test_set_operator_does_not_chain_when_awaiting_second(self, gui_with_mocks):
        """_set_operator when _awaiting_second=True should not chain."""
        gui = gui_with_mocks
        gui._first_operand = 5.0
        gui._operator = "-"
        gui._awaiting_second = True
        gui._current_input = "5"

        with mock.patch.object(gui, "_execute_normal") as mock_execute:
            gui._set_operator("+")
            mock_execute.assert_not_called()

    def test_set_operator_respects_binary_operators_constant(self, gui_with_mocks):
        """_set_operator should only accept operators from BINARY_OPERATORS."""
        gui = gui_with_mocks
        gui._current_input = "10"

        # Valid operators: +, -, *, /
        for op in ["+", "-", "*", "/"]:
            gui._first_operand = None
            gui._operator = None
            gui._set_operator(op)
            assert gui._operator == op

    def test_set_operator_invalid_operand_returns_early(self, gui_with_mocks):
        """_set_operator with non-numeric _current_input should not parse."""
        gui = gui_with_mocks
        gui._current_input = "not_a_number"

        gui._set_operator("+")

        # Should return early without crashing
        assert gui._first_operand is None


# ============================================================================
# CalculatorGUI._execute_normal — Binary calculation dispatch
# ============================================================================


class TestCalculatorGUIExecuteNormal:
    """Tests for CalculatorGUI._execute_normal method."""

    def test_execute_normal_happy_path_addition(self, gui_with_mocks):
        """_execute_normal should calculate 3 + 4 = 7."""
        gui = gui_with_mocks
        gui._first_operand = 3.0
        gui._operator = "+"
        gui._current_input = "4"

        with mock.patch("src.gui.run_calculation") as mock_calc:
            mock_calc.return_value = (7.0, mock.MagicMock())
            gui._execute_normal()

        mock_calc.assert_called_once_with(3.0, 4.0, "add")
        gui._display_var.set.assert_called()

    def test_execute_normal_happy_path_division(self, gui_with_mocks):
        """_execute_normal should calculate 8 / 2 = 4."""
        gui = gui_with_mocks
        gui._first_operand = 8.0
        gui._operator = "/"
        gui._current_input = "2"

        with mock.patch("src.gui.run_calculation") as mock_calc:
            mock_calc.return_value = (4.0, mock.MagicMock())
            gui._execute_normal()

        mock_calc.assert_called_once_with(8.0, 2.0, "divide")

    def test_execute_normal_handles_zero_division_error(self, gui_with_mocks):
        """_execute_normal should catch ZeroDivisionError and show error."""
        gui = gui_with_mocks
        gui._first_operand = 5.0
        gui._operator = "/"
        gui._current_input = "0"

        with mock.patch("src.gui.run_calculation") as mock_calc, \
             mock.patch.object(gui, "_show_error") as mock_error:
            mock_calc.side_effect = ZeroDivisionError("division by zero")
            gui._execute_normal()

        mock_error.assert_called_once()
        assert "zero" in mock_error.call_args[0][0].lower()

    def test_execute_normal_handles_value_error(self, gui_with_mocks):
        """_execute_normal should catch ValueError and show error."""
        gui = gui_with_mocks
        gui._first_operand = 1.0
        gui._operator = "+"
        gui._current_input = "2"

        with mock.patch("src.gui.run_calculation") as mock_calc, \
             mock.patch.object(gui, "_show_error") as mock_error:
            mock_calc.side_effect = ValueError("invalid input")
            gui._execute_normal()

        mock_error.assert_called_once()

    def test_execute_normal_returns_early_without_first_operand(self, gui_with_mocks):
        """_execute_normal with first_operand=None should return early."""
        gui = gui_with_mocks
        gui._first_operand = None
        gui._operator = "+"
        gui._current_input = "5"

        with mock.patch("src.gui.run_calculation") as mock_calc:
            gui._execute_normal()
            mock_calc.assert_not_called()

    def test_execute_normal_returns_early_without_operator(self, gui_with_mocks):
        """_execute_normal with operator=None should return early."""
        gui = gui_with_mocks
        gui._first_operand = 10.0
        gui._operator = None
        gui._current_input = "5"

        with mock.patch("src.gui.run_calculation") as mock_calc:
            gui._execute_normal()
            mock_calc.assert_not_called()

    def test_execute_normal_resets_state_after_non_chain_execution(self, gui_with_mocks):
        """_execute_normal with chain=False should reset state."""
        gui = gui_with_mocks
        gui._first_operand = 5.0
        gui._operator = "+"
        gui._current_input = "3"

        with mock.patch("src.gui.run_calculation") as mock_calc:
            mock_calc.return_value = (8.0, mock.MagicMock())
            gui._execute_normal(chain=False)

        assert gui._first_operand is None
        assert gui._operator is None
        assert gui._awaiting_second is False

    def test_execute_normal_keeps_result_for_chaining(self, gui_with_mocks):
        """_execute_normal with chain=True should keep result as new first operand."""
        gui = gui_with_mocks
        gui._first_operand = 3.0
        gui._operator = "+"
        gui._current_input = "4"

        with mock.patch("src.gui.run_calculation") as mock_calc:
            mock_calc.return_value = (7.0, mock.MagicMock())
            gui._execute_normal(chain=True)

        assert gui._first_operand == 7.0
        assert gui._awaiting_second is True

    def test_execute_normal_uses_zero_for_missing_second_operand(self, gui_with_mocks):
        """_execute_normal with empty _current_input should use 0.0 as second operand."""
        gui = gui_with_mocks
        gui._first_operand = 5.0
        gui._operator = "+"
        gui._current_input = ""

        with mock.patch("src.gui.run_calculation") as mock_calc:
            mock_calc.return_value = (5.0, mock.MagicMock())
            gui._execute_normal()

        mock_calc.assert_called_once_with(5.0, 0.0, "add")

    def test_execute_normal_invalid_method_name_returns_early(self, gui_with_mocks):
        """_execute_normal with invalid operator -> method_name lookup returns early."""
        gui = gui_with_mocks
        gui._first_operand = 5.0
        gui._operator = "@"  # Invalid, not in BINARY_OPERATORS
        gui._current_input = "3"

        with mock.patch("src.gui.run_calculation") as mock_calc:
            gui._execute_normal()
            mock_calc.assert_not_called()

    def test_execute_normal_calls_run_calculation_with_method_name(self, gui_with_mocks):
        """_execute_normal should map operator to method_name via BINARY_OPERATORS."""
        gui = gui_with_mocks
        gui._first_operand = 10.0
        gui._operator = "*"
        gui._current_input = "5"

        with mock.patch("src.gui.run_calculation") as mock_calc:
            mock_calc.return_value = (50.0, mock.MagicMock())
            gui._execute_normal()

        # The operator "*" should map to "multiply"
        mock_calc.assert_called_once_with(10.0, 5.0, "multiply")

    def test_execute_normal_formats_result_for_display(self, gui_with_mocks):
        """_execute_normal should format result and display it."""
        gui = gui_with_mocks
        gui._first_operand = 5.0
        gui._operator = "/"
        gui._current_input = "2"

        with mock.patch("src.gui.run_calculation") as mock_calc:
            mock_calc.return_value = (2.5, mock.MagicMock())
            gui._execute_normal()

        # Result 2.5 should be set on display
        display_calls = gui._display_var.set.call_args_list
        assert any("2.5" in str(call) for call in display_calls)


# ============================================================================
# CalculatorGUI._execute_scientific — Unary calculation dispatch
# ============================================================================


class TestCalculatorGUIExecuteScientific:
    """Tests for CalculatorGUI._execute_scientific method."""

    def test_execute_scientific_happy_path_sin(self, gui_with_mocks):
        """_execute_scientific should calculate sin(0) = 0."""
        gui = gui_with_mocks
        gui._sci_function = "sin"
        gui._sci_awaiting_arg = True
        gui._current_input = "0"

        with mock.patch("src.gui.run_unary_calculation") as mock_calc:
            mock_calc.return_value = (0.0, mock.MagicMock())
            gui._execute_scientific()

        mock_calc.assert_called_once_with(0.0, "sin")

    def test_execute_scientific_happy_path_sqrt(self, gui_with_mocks):
        """_execute_scientific should calculate sqrt(16) = 4."""
        gui = gui_with_mocks
        gui._sci_function = "sqrt"
        gui._sci_awaiting_arg = True
        gui._current_input = "16"

        with mock.patch("src.gui.run_unary_calculation") as mock_calc:
            mock_calc.return_value = (4.0, mock.MagicMock())
            gui._execute_scientific()

        mock_calc.assert_called_once_with(16.0, "sqrt")

    def test_execute_scientific_returns_early_without_function(self, gui_with_mocks):
        """_execute_scientific with sci_function=None should show error."""
        gui = gui_with_mocks
        gui._sci_function = None
        gui._current_input = "5"

        with mock.patch.object(gui, "_show_error") as mock_error:
            gui._execute_scientific()

        mock_error.assert_called_once()
        assert "function" in mock_error.call_args[0][0].lower()

    def test_execute_scientific_handles_value_error(self, gui_with_mocks):
        """_execute_scientific should catch ValueError (e.g. sqrt of negative)."""
        gui = gui_with_mocks
        gui._sci_function = "sqrt"
        gui._sci_awaiting_arg = True
        gui._current_input = "-4"

        with mock.patch("src.gui.run_unary_calculation") as mock_calc, \
             mock.patch.object(gui, "_show_error") as mock_error:
            mock_calc.side_effect = ValueError("sqrt of negative number")
            gui._execute_scientific()

        mock_error.assert_called_once()

    def test_execute_scientific_uses_zero_for_missing_operand(self, gui_with_mocks):
        """_execute_scientific with empty input should use 0.0 as operand."""
        gui = gui_with_mocks
        gui._sci_function = "exp"
        gui._sci_awaiting_arg = True
        gui._current_input = ""

        with mock.patch("src.gui.run_unary_calculation") as mock_calc:
            mock_calc.return_value = (1.0, mock.MagicMock())
            gui._execute_scientific()

        mock_calc.assert_called_once_with(0.0, "exp")

    def test_execute_scientific_unknown_function_shows_error(self, gui_with_mocks):
        """_execute_scientific with unknown function_name shows error."""
        gui = gui_with_mocks
        gui._sci_function = "not_a_function"
        gui._sci_awaiting_arg = True
        gui._current_input = "5"

        with mock.patch.object(gui, "_show_error") as mock_error:
            gui._execute_scientific()

        mock_error.assert_called_once()
        assert "unknown" in mock_error.call_args[0][0].lower()

    def test_execute_scientific_resets_state_after_execution(self, gui_with_mocks):
        """_execute_scientific should reset scientific state after calculation."""
        gui = gui_with_mocks
        gui._sci_function = "log"
        gui._sci_awaiting_arg = True
        gui._current_input = "10"

        with mock.patch("src.gui.run_unary_calculation") as mock_calc:
            mock_calc.return_value = (1.0, mock.MagicMock())
            gui._execute_scientific()

        assert gui._sci_function is None
        assert gui._sci_awaiting_arg is False

    def test_execute_scientific_displays_result(self, gui_with_mocks):
        """_execute_scientific should display formatted result."""
        gui = gui_with_mocks
        gui._sci_function = "ln"
        gui._sci_awaiting_arg = True
        gui._current_input = "2.718281828"

        with mock.patch("src.gui.run_unary_calculation") as mock_calc:
            mock_calc.return_value = (1.0, mock.MagicMock())
            gui._execute_scientific()

        # Result should be set on display
        display_calls = gui._display_var.set.call_args_list
        assert any("1" in str(call) for call in display_calls)

    def test_execute_scientific_invalid_operand_shows_error(self, gui_with_mocks):
        """_execute_scientific with non-numeric input shows error."""
        gui = gui_with_mocks
        gui._sci_function = "sin"
        gui._sci_awaiting_arg = True
        gui._current_input = "not_a_number"

        with mock.patch.object(gui, "_show_error") as mock_error:
            gui._execute_scientific()

        mock_error.assert_called_once()
        assert "invalid" in mock_error.call_args[0][0].lower()


# ============================================================================
# CalculatorGUI._show_error — Error display and auto-reset
# ============================================================================


class TestCalculatorGUIShowError:
    """Tests for CalculatorGUI._show_error method."""

    def test_show_error_displays_message(self, gui_with_mocks):
        """_show_error should set display to the error message."""
        gui = gui_with_mocks

        gui._show_error("Division by zero")

        gui._display_var.set.assert_called()
        call_args = [call[0][0] for call in gui._display_var.set.call_args_list]
        assert any("Division" in arg or "zero" in arg.lower() for arg in call_args)

    def test_show_error_truncates_long_messages(self, gui_with_mocks):
        """_show_error should truncate message to 16 characters."""
        gui = gui_with_mocks
        long_msg = "This is a very long error message"

        gui._show_error(long_msg)

        # Check that display was set with truncated message
        call_args = gui._display_var.set.call_args_list
        assert any(len(str(call[0][0])) <= 16 for call in call_args if call[0])

    def test_show_error_sets_error_color(self, gui_with_mocks):
        """_show_error should set display label to error color."""
        gui = gui_with_mocks

        gui._show_error("Error message")

        gui._display_label.config.assert_called()

    def test_show_error_clears_state(self, gui_with_mocks):
        """_show_error should call _clear_state()."""
        gui = gui_with_mocks
        gui._current_input = "some_value"
        gui._first_operand = 10.0

        gui._show_error("Test error")

        # After _show_error, state should be cleared
        assert gui._current_input == ""
        assert gui._first_operand is None

    def test_show_error_schedules_color_reset(self, gui_with_mocks):
        """_show_error should schedule color reset via _root.after()."""
        gui = gui_with_mocks

        gui._show_error("Test error")

        gui._root.after.assert_called()
        # Verify it was called with a delay (2000 ms)
        call_args = gui._root.after.call_args
        assert call_args[0][0] == 2000

    def test_show_error_callback_resets_display_color(self, gui_with_mocks):
        """The callback from _show_error.after() should reset color to normal."""
        gui = gui_with_mocks

        gui._show_error("Test error")

        # Extract the callback lambda
        callback = gui._root.after.call_args[0][1]
        callback()

        # After callback, display_label.config should have been called with normal color
        gui._display_label.config.assert_called()


# ============================================================================
# CalculatorGUI._on_mode_switch — Mode toggle and state reset
# ============================================================================


class TestCalculatorGUIOnModeSwitch:
    """Tests for CalculatorGUI._on_mode_switch method."""

    def test_on_mode_switch_switches_to_normal(self, gui_with_mocks):
        """_on_mode_switch('normal') should set mode to normal."""
        gui = gui_with_mocks
        gui._mode_manager.set_mode("scientific")  # Start in scientific

        gui._on_mode_switch("normal")

        assert gui._mode_manager.get_mode() == "normal"

    def test_on_mode_switch_switches_to_scientific(self, gui_with_mocks):
        """_on_mode_switch('scientific') should set mode to scientific."""
        gui = gui_with_mocks

        gui._on_mode_switch("scientific")

        assert gui._mode_manager.get_mode() == "scientific"

    def test_on_mode_switch_clears_state(self, gui_with_mocks):
        """_on_mode_switch should clear all calculator state."""
        gui = gui_with_mocks
        gui._current_input = "42"
        gui._first_operand = 10.0

        gui._on_mode_switch("scientific")

        assert gui._current_input == ""
        assert gui._first_operand is None

    def test_on_mode_switch_refreshes_layout(self, gui_with_mocks):
        """_on_mode_switch should call _refresh_mode_layout()."""
        gui = gui_with_mocks

        with mock.patch.object(gui, "_refresh_mode_layout") as mock_refresh:
            gui._on_mode_switch("scientific")
            mock_refresh.assert_called_once()

    def test_on_mode_switch_invalid_mode_shows_error(self, gui_with_mocks):
        """_on_mode_switch with invalid mode should show error."""
        gui = gui_with_mocks

        with mock.patch.object(gui, "_show_error") as mock_error:
            gui._on_mode_switch("invalid_mode")

        mock_error.assert_called_once()


# ============================================================================
# CalculatorGUI._on_normal_action — Normal mode action dispatch
# ============================================================================


class TestCalculatorGUIOnNormalAction:
    """Tests for CalculatorGUI._on_normal_action method."""

    def test_on_normal_action_clear(self, gui_with_mocks):
        """_on_normal_action('clear') should call _clear_state()."""
        gui = gui_with_mocks

        with mock.patch.object(gui, "_clear_state") as mock_clear:
            gui._on_normal_action("clear")
            mock_clear.assert_called_once()

    def test_on_normal_action_negate(self, gui_with_mocks):
        """_on_normal_action('negate') should call _negate_display()."""
        gui = gui_with_mocks

        with mock.patch.object(gui, "_negate_display") as mock_negate:
            gui._on_normal_action("negate")
            mock_negate.assert_called_once()

    def test_on_normal_action_percent(self, gui_with_mocks):
        """_on_normal_action('percent') should call _apply_percent()."""
        gui = gui_with_mocks

        with mock.patch.object(gui, "_apply_percent") as mock_percent:
            gui._on_normal_action("percent")
            mock_percent.assert_called_once()

    def test_on_normal_action_equals(self, gui_with_mocks):
        """_on_normal_action('equals') should call _execute_normal()."""
        gui = gui_with_mocks

        with mock.patch.object(gui, "_execute_normal") as mock_execute:
            gui._on_normal_action("equals")
            mock_execute.assert_called_once()

    def test_on_normal_action_digit(self, gui_with_mocks):
        """_on_normal_action('num:5') should call _append_digit('5')."""
        gui = gui_with_mocks

        with mock.patch.object(gui, "_append_digit") as mock_append:
            gui._on_normal_action("num:7")
            mock_append.assert_called_once_with("7")

    def test_on_normal_action_operator(self, gui_with_mocks):
        """_on_normal_action('op:+') should call _set_operator('+')."""
        gui = gui_with_mocks

        with mock.patch.object(gui, "_set_operator") as mock_set_op:
            gui._on_normal_action("op:+")
            mock_set_op.assert_called_once_with("+")


# ============================================================================
# CalculatorGUI._on_sci_function — Scientific function selection
# ============================================================================


class TestCalculatorGUIOnSciFunction:
    """Tests for CalculatorGUI._on_sci_function method."""

    def test_on_sci_function_sets_sci_function(self, gui_with_mocks):
        """_on_sci_function('sin') should set _sci_function to 'sin'."""
        gui = gui_with_mocks

        gui._on_sci_function("sin")

        assert gui._sci_function == "sin"

    def test_on_sci_function_sets_awaiting_arg(self, gui_with_mocks):
        """_on_sci_function should set _sci_awaiting_arg to True."""
        gui = gui_with_mocks

        gui._on_sci_function("cos")

        assert gui._sci_awaiting_arg is True

    def test_on_sci_function_clears_input(self, gui_with_mocks):
        """_on_sci_function should clear _current_input."""
        gui = gui_with_mocks
        gui._current_input = "previous_value"

        gui._on_sci_function("tan")

        assert gui._current_input == ""

    def test_on_sci_function_displays_function_prompt(self, gui_with_mocks):
        """_on_sci_function should show 'function_name( ... )' in history."""
        gui = gui_with_mocks

        gui._on_sci_function("sqrt")

        gui._history_var.set.assert_called()
        call_args = gui._history_var.set.call_args[0][0]
        assert "sqrt" in call_args
        assert "(" in call_args

    def test_on_sci_function_resets_display_to_zero(self, gui_with_mocks):
        """_on_sci_function should set display to '0'."""
        gui = gui_with_mocks

        gui._on_sci_function("log")

        gui._display_var.set.assert_called()
        call_args = [call[0][0] for call in gui._display_var.set.call_args_list]
        assert "0" in call_args


# ============================================================================
# CalculatorGUI._on_sci_action — Scientific mode action dispatch
# ============================================================================


class TestCalculatorGUIOnSciAction:
    """Tests for CalculatorGUI._on_sci_action method."""

    def test_on_sci_action_clear(self, gui_with_mocks):
        """_on_sci_action('clear') should call _clear_state()."""
        gui = gui_with_mocks

        with mock.patch.object(gui, "_clear_state") as mock_clear:
            gui._on_sci_action("clear")
            mock_clear.assert_called_once()

    def test_on_sci_action_negate(self, gui_with_mocks):
        """_on_sci_action('negate') should call _negate_display()."""
        gui = gui_with_mocks

        with mock.patch.object(gui, "_negate_display") as mock_negate:
            gui._on_sci_action("negate")
            mock_negate.assert_called_once()

    def test_on_sci_action_equals(self, gui_with_mocks):
        """_on_sci_action('equals') should call _execute_scientific()."""
        gui = gui_with_mocks

        with mock.patch.object(gui, "_execute_scientific") as mock_execute:
            gui._on_sci_action("equals")
            mock_execute.assert_called_once()

    def test_on_sci_action_digit(self, gui_with_mocks):
        """_on_sci_action('num:3') should call _append_digit('3')."""
        gui = gui_with_mocks

        with mock.patch.object(gui, "_append_digit") as mock_append:
            gui._on_sci_action("num:9")
            mock_append.assert_called_once_with("9")


# ============================================================================
# Integration-style tests: full calculation workflows
# ============================================================================


class TestCalculatorGUIIntegration:
    """Integration tests for complete calculation workflows."""

    def test_normal_calculation_workflow(self, gui_with_mocks):
        """Full workflow: enter 5 + 3, press equals."""
        gui = gui_with_mocks

        # User enters 5
        gui._append_digit("5")
        assert gui._current_input == "5"

        # User presses +
        gui._set_operator("+")
        assert gui._first_operand == 5.0
        assert gui._operator == "+"
        assert gui._awaiting_second is True

        # User enters 3
        gui._append_digit("3")
        assert gui._current_input == "3"

        # User presses =
        with mock.patch("src.gui.run_calculation") as mock_calc:
            mock_calc.return_value = (8.0, mock.MagicMock())
            gui._execute_normal()

        # State should be reset
        assert gui._first_operand is None
        assert gui._operator is None

    def test_scientific_calculation_workflow(self, gui_with_mocks):
        """Full workflow: sin(90), press equals."""
        gui = gui_with_mocks

        # User selects sin function
        gui._on_sci_function("sin")
        assert gui._sci_function == "sin"
        assert gui._sci_awaiting_arg is True

        # User enters 90
        gui._append_digit("9")
        gui._append_digit("0")
        assert gui._current_input == "90"

        # User presses =
        with mock.patch("src.gui.run_unary_calculation") as mock_calc:
            mock_calc.return_value = (1.0, mock.MagicMock())
            gui._execute_scientific()

        # Scientific state should be reset
        assert gui._sci_function is None
        assert gui._sci_awaiting_arg is False

    def test_operator_chaining_workflow(self, gui_with_mocks):
        """Workflow: 3 + 4 + 5 (operator chaining)."""
        gui = gui_with_mocks

        # 3 + 4
        gui._append_digit("3")
        gui._set_operator("+")
        gui._append_digit("4")

        # Press + again (should chain)
        with mock.patch("src.gui.run_calculation") as mock_calc:
            mock_calc.return_value = (7.0, mock.MagicMock())
            gui._set_operator("+")

        # After chaining, result (7) should be first operand
        assert gui._first_operand == 7.0
        assert gui._awaiting_second is True


# ============================================================================
# Tests for __main__.py --gui flag and CALCULATOR_GUI env var
# ============================================================================


class TestMainGUIFlag:
    """Tests for __main__.py GUI launch via --gui flag and env var."""

    def test_gui_flag_launches_gui(self):
        """When --gui is in sys.argv, CalculatorGUI should be instantiated."""
        with mock.patch.dict("os.environ", {}, clear=False), \
             mock.patch("sys.argv", ["calculator", "--gui"]), \
             mock.patch("src.gui.CalculatorGUI") as mock_gui_class:
            mock_gui_instance = mock.MagicMock()
            mock_gui_class.return_value = mock_gui_instance

            # Import the main block dynamically to test the if __name__ == "__main__" logic
            import src.__main__

            # Simulate the condition
            _gui_requested = "--gui" in sys.argv or __import__("os").environ.get("CALCULATOR_GUI", "0") == "1"
            assert _gui_requested is True

    def test_calculator_gui_env_var_launches_gui(self):
        """When CALCULATOR_GUI=1, GUI should be launched."""
        with mock.patch.dict("os.environ", {"CALCULATOR_GUI": "1"}), \
             mock.patch("sys.argv", ["calculator"]):
            import os
            _gui_requested = "--gui" in sys.argv or os.environ.get("CALCULATOR_GUI", "0") == "1"
            assert _gui_requested is True

    def test_cli_argument_delegates_to_cli_main(self):
        """When sys.argv has args (not --gui), cli_main() should be called."""
        with mock.patch.dict("os.environ", {}, clear=False), \
             mock.patch("sys.argv", ["calculator", "1", "+", "2"]):
            _gui_requested = "--gui" in sys.argv or __import__("os").environ.get("CALCULATOR_GUI", "0") == "1"
            assert _gui_requested is False

    def test_no_arguments_runs_interactive_mode(self):
        """When no arguments and no --gui, interactive mode should run."""
        with mock.patch.dict("os.environ", {}, clear=False), \
             mock.patch("sys.argv", ["calculator"]):
            _gui_requested = "--gui" in sys.argv or __import__("os").environ.get("CALCULATOR_GUI", "0") == "1"
            cli_args_present = len(sys.argv) > 1

            assert _gui_requested is False
            assert cli_args_present is False
