"""test_gui.py — comprehensive tests for the CalculatorGUI module.

Tests the CalculatorGUI class and the --gui flag in main.py.
Uses mocking to work in headless CI without tkinter.
"""

import pytest
import sys
from unittest.mock import patch, MagicMock, call, Mock
import importlib.util

from src.calculator import Calculator
from src.input_handler import ExpressionParser, InputValidator, OperationNotAvailableInModeError


# Check if tkinter is available
tkinter_available = importlib.util.find_spec("tkinter") is not None

# If tkinter is not available, we'll mock it before importing gui.py
if not tkinter_available:
    # Create a mock StringVar that properly stores values
    class MockStringVar:
        def __init__(self, value=""):
            self._value = value

        def set(self, value):
            self._value = value

        def get(self):
            return self._value

    # Create a mock Tk that properly responds to methods
    class MockTk:
        def __init__(self):
            self._title = ""
            self._resizable = (False, False)

        def title(self, text=None):
            if text is None:
                return self._title
            self._title = text

        def resizable(self, width=None, height=None):
            if width is None:
                return self._resizable
            self._resizable = (width, height)

        def withdraw(self):
            pass

        def destroy(self):
            pass

        def columnconfigure(self, *args, **kwargs):
            pass

        def rowconfigure(self, *args, **kwargs):
            pass

        def mainloop(self):
            pass

    # Create a mock tkinter module
    mock_tk = MagicMock()
    mock_tk.Tk = MockTk
    mock_tk.StringVar = MockStringVar
    mock_tk.Entry = MagicMock()
    mock_tk.Frame = MagicMock()
    mock_tk.Label = MagicMock()
    mock_tk.Button = MagicMock()
    mock_tk.OptionMenu = MagicMock()
    sys.modules["tkinter"] = mock_tk

# Now we can safely import tkinter
import tkinter as tk

# Now import CalculatorGUI
from src.gui import CalculatorGUI


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def calculator():
    """Provide a fresh Calculator instance for tests."""
    return Calculator()


@pytest.fixture
def gui_app(calculator):
    """Provide a CalculatorGUI instance with a test calculator.

    The GUI is created with withdraw() to prevent window from showing,
    and is destroyed after the test completes.
    """
    app = CalculatorGUI(calculator)
    if hasattr(app, 'withdraw'):
        app.withdraw()  # Hide the window if available
    yield app
    if hasattr(app, 'destroy'):
        app.destroy()  # Clean up if available


@pytest.fixture
def gui_app_default():
    """Provide a CalculatorGUI instance with default Calculator."""
    app = CalculatorGUI()
    if hasattr(app, 'withdraw'):
        app.withdraw()
    yield app
    if hasattr(app, 'destroy'):
        app.destroy()


# ============================================================================
# Instantiation Tests
# ============================================================================


class TestGUIInstantiation:
    """Tests for CalculatorGUI initialization."""

    def test_gui_instantiation_no_args(self, gui_app_default):
        """Test CalculatorGUI() creates instance with default Calculator."""
        assert gui_app_default is not None
        assert isinstance(gui_app_default._calculator, Calculator)
        assert gui_app_default._calculator._mode == "advanced"
        assert isinstance(gui_app_default._parser, ExpressionParser)
        assert isinstance(gui_app_default._validator, InputValidator)

    def test_gui_instantiation_with_calculator(self, calculator, gui_app):
        """Test CalculatorGUI(calculator) stores injected Calculator instance."""
        assert gui_app._calculator is calculator
        assert gui_app._expression == ""
        assert gui_app._display_var.get() == ""

    def test_gui_title_set(self, gui_app):
        """Test that the window title is set to 'Calculator'."""
        assert gui_app.title() == "Calculator"

    def test_gui_not_resizable(self, gui_app):
        """Test that the window is not resizable."""
        # resizable() returns a tuple of (width, height) booleans
        resizable_w, resizable_h = gui_app.resizable()
        assert resizable_w == 0  # False, not resizable
        assert resizable_h == 0  # False, not resizable


# ============================================================================
# Display and Expression Management Tests
# ============================================================================


class TestGUIClear:
    """Tests for the _clear() method."""

    def test_gui_clear_empty_expression(self, gui_app):
        """Test _clear() on already empty expression."""
        gui_app._expression = ""
        gui_app._clear()
        assert gui_app._expression == ""
        assert gui_app._display_var.get() == ""

    def test_gui_clear_with_content(self, gui_app):
        """Test _clear() resets expression and display after appending."""
        gui_app._append("5")
        gui_app._append("3")
        assert gui_app._expression == "53"

        gui_app._clear()
        assert gui_app._expression == ""
        assert gui_app._display_var.get() == ""

    def test_gui_clear_after_operator(self, gui_app):
        """Test _clear() resets expression with operator."""
        gui_app._append_operator("+")
        assert gui_app._expression == "add "

        gui_app._clear()
        assert gui_app._expression == ""
        assert gui_app._display_var.get() == ""


class TestGUIBackspace:
    """Tests for the _backspace() method."""

    def test_gui_backspace_on_empty_string(self, gui_app):
        """Test _backspace() on empty expression does not crash."""
        gui_app._expression = ""
        gui_app._backspace()  # Should not raise
        assert gui_app._expression == ""
        assert gui_app._display_var.get() == ""

    def test_gui_backspace_single_character(self, gui_app):
        """Test _backspace() removes last character."""
        gui_app._append("5")
        assert gui_app._expression == "5"

        gui_app._backspace()
        assert gui_app._expression == ""
        assert gui_app._display_var.get() == ""

    def test_gui_backspace_multiple_characters(self, gui_app):
        """Test _backspace() removes exactly the last character."""
        gui_app._append("5")
        gui_app._append("3")
        assert gui_app._expression == "53"

        gui_app._backspace()
        assert gui_app._expression == "5"
        assert gui_app._display_var.get() == "5"

    def test_gui_backspace_with_space(self, gui_app):
        """Test _backspace() removes space character."""
        gui_app._expression = "add "
        gui_app._backspace()
        assert gui_app._expression == "add"
        assert gui_app._display_var.get() == "add"


class TestGUIAppend:
    """Tests for the _append() method."""

    def test_gui_append_single_digit(self, gui_app):
        """Test _append() with single digit."""
        gui_app._append("5")
        assert gui_app._expression == "5"
        assert gui_app._display_var.get() == "5"

    @pytest.mark.parametrize("digit", ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
    def test_gui_append_all_digits(self, gui_app, digit):
        """Test _append() with all digit characters."""
        gui_app._append(digit)
        assert gui_app._expression == digit
        assert gui_app._display_var.get() == digit

    def test_gui_append_multiple_digits(self, gui_app):
        """Test _append() with multiple consecutive digits."""
        gui_app._append("5")
        gui_app._append("3")
        assert gui_app._expression == "53"
        assert gui_app._display_var.get() == "53"

    def test_gui_append_decimal_point(self, gui_app):
        """Test _append() with decimal point."""
        gui_app._append("5")
        gui_app._append(".")
        gui_app._append("3")
        assert gui_app._expression == "5.3"
        assert gui_app._display_var.get() == "5.3"

    def test_gui_append_long_number(self, gui_app):
        """Test _append() builds a long number correctly."""
        for digit in "123456789":
            gui_app._append(digit)
        assert gui_app._expression == "123456789"
        assert gui_app._display_var.get() == "123456789"


# ============================================================================
# Operator Tests
# ============================================================================


class TestGUIAppendOperator:
    """Tests for the _append_operator() method."""

    def test_gui_append_operator_plus_on_empty(self, gui_app):
        """Test _append_operator('+') on empty expression."""
        gui_app._append_operator("+")
        assert gui_app._expression == "add "
        assert gui_app._display_var.get() == "add "

    def test_gui_append_operator_minus_on_empty(self, gui_app):
        """Test _append_operator('-') on empty expression."""
        gui_app._append_operator("-")
        assert gui_app._expression == "subtract "
        assert gui_app._display_var.get() == "subtract "

    def test_gui_append_operator_multiply_on_empty(self, gui_app):
        """Test _append_operator('*') on empty expression."""
        gui_app._append_operator("*")
        assert gui_app._expression == "multiply "
        assert gui_app._display_var.get() == "multiply "

    def test_gui_append_operator_divide_on_empty(self, gui_app):
        """Test _append_operator('/') on empty expression."""
        gui_app._append_operator("/")
        assert gui_app._expression == "divide "
        assert gui_app._display_var.get() == "divide "

    def test_gui_append_operator_plus_with_operand(self, gui_app):
        """Test _append_operator('+') prepends operation before single operand."""
        gui_app._append("5")
        gui_app._append_operator("+")
        assert gui_app._expression == "add 5 "
        assert gui_app._display_var.get() == "add 5 "

    def test_gui_append_operator_after_operation_and_operand(self, gui_app):
        """Test _append_operator() appends space when op + operand exist."""
        gui_app._append("5")
        gui_app._append_operator("+")
        gui_app._append("3")
        gui_app._append_operator("+")
        # At this point: "5" -> "add 5 " -> "add 5 3" -> "add 5 3 "
        assert gui_app._expression == "add 5 3 "
        assert gui_app._display_var.get() == "add 5 3 "

    @pytest.mark.parametrize("operator,expected_op", [
        ("+", "add"),
        ("-", "subtract"),
        ("*", "multiply"),
        ("/", "divide"),
    ])
    def test_gui_append_operator_translations(self, gui_app, operator, expected_op):
        """Test _append_operator() translates symbols to word forms."""
        gui_app._append_operator(operator)
        assert gui_app._expression.startswith(expected_op)

    def test_gui_append_operator_with_whitespace(self, gui_app):
        """Test _append_operator() handles existing whitespace."""
        gui_app._expression = "  5  "
        gui_app._append_operator("+")
        # Should strip and prepend operation
        assert gui_app._expression == "add 5 "


# ============================================================================
# Evaluation Tests
# ============================================================================


class TestGUIEvaluateHappyPath:
    """Tests for _evaluate() with valid expressions."""

    def test_gui_evaluate_addition(self, gui_app):
        """Test _evaluate() with 'add 5 3' shows '8'."""
        gui_app._expression = "add 5 3"
        gui_app._evaluate()
        assert gui_app._display_var.get() == "8"
        assert gui_app._expression == "8"

    def test_gui_evaluate_subtraction(self, gui_app):
        """Test _evaluate() with 'subtract 10 4' shows '6'."""
        gui_app._expression = "subtract 10 4"
        gui_app._evaluate()
        assert gui_app._display_var.get() == "6"
        assert gui_app._expression == "6"

    def test_gui_evaluate_multiplication(self, gui_app):
        """Test _evaluate() with 'multiply 2 3' shows '6'."""
        gui_app._expression = "multiply 2 3"
        gui_app._evaluate()
        assert gui_app._display_var.get() == "6"
        assert gui_app._expression == "6"

    def test_gui_evaluate_division(self, gui_app):
        """Test _evaluate() with 'divide 10 2' shows result."""
        gui_app._expression = "divide 10 2"
        gui_app._evaluate()
        # Division returns float, so "5.0" not "5"
        assert gui_app._display_var.get() == "5.0"
        assert gui_app._expression == "5.0"

    def test_gui_evaluate_division_float_result(self, gui_app):
        """Test _evaluate() with division producing float."""
        gui_app._expression = "divide 7 2"
        gui_app._evaluate()
        assert gui_app._display_var.get() == "3.5"
        assert gui_app._expression == "3.5"

    def test_gui_evaluate_square(self, gui_app):
        """Test _evaluate() with square operation."""
        gui_app._expression = "square 4"
        gui_app._evaluate()
        assert gui_app._display_var.get() == "16"
        assert gui_app._expression == "16"

    def test_gui_evaluate_power(self, gui_app):
        """Test _evaluate() with power operation."""
        gui_app._expression = "power 2 3"
        gui_app._evaluate()
        assert gui_app._display_var.get() == "8"
        assert gui_app._expression == "8"

    def test_gui_evaluate_result_becomes_new_expression(self, gui_app):
        """Test that result becomes the new expression for chaining."""
        gui_app._expression = "add 2 3"
        gui_app._evaluate()
        assert gui_app._expression == "5"
        # User can now build on the result
        gui_app._append_operator("+")
        assert gui_app._expression == "add 5 "


class TestGUIEvaluateErrors:
    """Tests for _evaluate() error handling."""

    def test_gui_evaluate_empty_expression(self, gui_app):
        """Test _evaluate() on empty expression returns without crashing."""
        gui_app._expression = ""
        gui_app._evaluate()  # Should not crash
        # Display should remain empty
        assert gui_app._display_var.get() == ""

    def test_gui_evaluate_whitespace_only_expression(self, gui_app):
        """Test _evaluate() on whitespace-only expression."""
        gui_app._expression = "   "
        gui_app._evaluate()  # Should not crash
        assert gui_app._display_var.get() == ""

    def test_gui_evaluate_division_by_zero(self, gui_app):
        """Test _evaluate() with division by zero shows error."""
        gui_app._expression = "divide 1 0"
        gui_app._evaluate()
        display = gui_app._display_var.get()
        assert display.startswith("Error:")
        assert "division by zero" in display

    def test_gui_evaluate_unknown_operation(self, gui_app):
        """Test _evaluate() with unknown operation shows error."""
        gui_app._expression = "blah 5"
        gui_app._evaluate()
        display = gui_app._display_var.get()
        # Error message starts with "Validation error:" or "Input error:"
        assert display.startswith("Validation error:") or display.startswith("Input error:")

    def test_gui_evaluate_malformed_operand(self, gui_app):
        """Test _evaluate() with non-numeric operand shows error."""
        gui_app._expression = "add abc 5"
        gui_app._evaluate()
        display = gui_app._display_var.get()
        assert display.startswith("Input error:")

    def test_gui_evaluate_wrong_operand_count(self, gui_app):
        """Test _evaluate() with wrong operand count shows error."""
        gui_app._expression = "add 5"  # add needs 2 operands
        gui_app._evaluate()
        display = gui_app._display_var.get()
        assert display.startswith("Validation error:")

    def test_gui_evaluate_operation_unavailable_in_mode(self, calculator, gui_app):
        """Test _evaluate() with operation unavailable in current mode."""
        # Set calculator to basic mode (only has add, subtract, multiply, divide)
        calculator.set_mode("basic")
        gui_app._expression = "square 5"  # square not in basic mode
        gui_app._evaluate()
        display = gui_app._display_var.get()
        # Error message shows the operation is not available
        assert "not available" in display and "basic" in display


class TestGUIEvaluateEdgeCases:
    """Tests for _evaluate() edge cases."""

    def test_gui_evaluate_negative_numbers(self, gui_app):
        """Test _evaluate() with negative operands."""
        gui_app._expression = "add -5 3"
        gui_app._evaluate()
        assert gui_app._display_var.get() == "-2"

    def test_gui_evaluate_floating_point(self, gui_app):
        """Test _evaluate() with floating point operands."""
        gui_app._expression = "divide 7 3"
        gui_app._evaluate()
        result = gui_app._display_var.get()
        # Should be approximately 2.333...
        assert "2.333" in result or "2.33" in result

    def test_gui_evaluate_large_numbers(self, gui_app):
        """Test _evaluate() with very large numbers."""
        gui_app._expression = "add 1000000000 500000000"
        gui_app._evaluate()
        assert gui_app._display_var.get() == "1500000000"

    def test_gui_evaluate_very_small_numbers(self, gui_app):
        """Test _evaluate() with very small numbers."""
        gui_app._expression = "add 0.00001 0.00002"
        gui_app._evaluate()
        result = gui_app._display_var.get()
        # Result is approximately 3e-5, may be in scientific notation
        assert float(result) == pytest.approx(3e-5)

    def test_gui_evaluate_case_insensitive_operation(self, gui_app):
        """Test _evaluate() accepts case-insensitive operations."""
        gui_app._expression = "ADD 5 3"
        gui_app._evaluate()
        assert gui_app._display_var.get() == "8"

    def test_gui_evaluate_extra_whitespace(self, gui_app):
        """Test _evaluate() handles extra whitespace."""
        gui_app._expression = "  add   5   3  "
        gui_app._evaluate()
        assert gui_app._display_var.get() == "8"


# ============================================================================
# Mode Change Tests
# ============================================================================


class TestGUIModeChange:
    """Tests for mode switching in GUI."""

    def test_gui_mode_change_basic(self, calculator, gui_app):
        """Test mode change to 'basic' calls calculator.set_mode()."""
        calculator._mode = "advanced"
        gui_app._on_mode_change("basic")
        assert calculator._mode == "basic"

    def test_gui_mode_change_scientific(self, calculator, gui_app):
        """Test mode change to 'scientific'."""
        gui_app._on_mode_change("scientific")
        assert calculator._mode == "scientific"

    def test_gui_mode_change_invalid_mode(self, gui_app):
        """Test invalid mode change shows error in display."""
        gui_app._on_mode_change("invalid_mode")
        display = gui_app._display_var.get()
        assert display.startswith("Mode error:")

    def test_gui_mode_change_preserves_expression(self, calculator, gui_app):
        """Test that mode change does not affect current expression."""
        gui_app._expression = "add 5 3"
        gui_app._on_mode_change("basic")
        assert gui_app._expression == "add 5 3"

    @pytest.mark.parametrize("mode", ["basic", "advanced", "scientific"])
    def test_gui_mode_change_all_valid_modes(self, calculator, gui_app, mode):
        """Test mode change to all valid modes."""
        gui_app._on_mode_change(mode)
        assert calculator._mode == mode
        assert gui_app._display_var.get() == ""  # No error


# ============================================================================
# Button Event Handler Tests
# ============================================================================


class TestGUIButtonHandler:
    """Tests for the _on_button() event dispatcher."""

    def test_gui_button_clear(self, gui_app):
        """Test pressing 'C' button calls _clear()."""
        gui_app._append("5")
        gui_app._on_button("C")
        assert gui_app._expression == ""
        assert gui_app._display_var.get() == ""

    def test_gui_button_backspace(self, gui_app):
        """Test pressing '←' button calls _backspace()."""
        gui_app._append("5")
        gui_app._append("3")
        gui_app._on_button("←")
        assert gui_app._expression == "5"

    def test_gui_button_equals(self, gui_app):
        """Test pressing '=' button calls _evaluate()."""
        gui_app._expression = "add 5 3"
        gui_app._on_button("=")
        assert gui_app._display_var.get() == "8"

    def test_gui_button_operator_plus(self, gui_app):
        """Test pressing '+' button calls _append_operator()."""
        gui_app._on_button("+")
        assert gui_app._expression == "add "

    def test_gui_button_operator_minus(self, gui_app):
        """Test pressing '-' button calls _append_operator()."""
        gui_app._on_button("-")
        assert gui_app._expression == "subtract "

    def test_gui_button_operator_multiply(self, gui_app):
        """Test pressing '*' button calls _append_operator()."""
        gui_app._on_button("*")
        assert gui_app._expression == "multiply "

    def test_gui_button_operator_divide(self, gui_app):
        """Test pressing '/' button calls _append_operator()."""
        gui_app._on_button("/")
        assert gui_app._expression == "divide "

    @pytest.mark.parametrize("digit", ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
    def test_gui_button_digit(self, gui_app, digit):
        """Test pressing digit buttons appends to expression."""
        gui_app._on_button(digit)
        assert gui_app._expression == digit

    def test_gui_button_decimal(self, gui_app):
        """Test pressing '.' button appends decimal point."""
        gui_app._on_button("5")
        gui_app._on_button(".")
        gui_app._on_button("3")
        assert gui_app._expression == "5.3"


# ============================================================================
# Integration Tests
# ============================================================================


class TestGUIIntegration:
    """Integration tests combining multiple GUI features."""

    def test_gui_full_calculation_sequence(self, gui_app):
        """Test complete user sequence: input, calculate, continue."""
        # User types: 5 + 3 =
        gui_app._on_button("5")
        assert gui_app._expression == "5"

        gui_app._on_button("+")
        assert gui_app._expression == "add 5 "

        gui_app._on_button("3")
        assert gui_app._expression == "add 5 3"

        gui_app._on_button("=")
        assert gui_app._expression == "8"
        assert gui_app._display_var.get() == "8"

    def test_gui_chain_calculations(self, gui_app):
        """Test chaining multiple calculations."""
        # 5 + 3 = 8
        gui_app._expression = "add 5 3"
        gui_app._on_button("=")
        assert gui_app._expression == "8"

        # 8 * 2 = 16
        gui_app._on_button("*")
        gui_app._on_button("2")
        gui_app._on_button("=")
        assert gui_app._expression == "16"
        assert gui_app._display_var.get() == "16"

    def test_gui_clear_after_result(self, gui_app):
        """Test clearing after displaying a result."""
        gui_app._expression = "add 5 3"
        gui_app._on_button("=")
        assert gui_app._expression == "8"

        gui_app._on_button("C")
        assert gui_app._expression == ""
        assert gui_app._display_var.get() == ""

    def test_gui_backspace_and_recalculate(self, gui_app):
        """Test backspacing and recalculating."""
        gui_app._on_button("5")
        gui_app._on_button("+")
        gui_app._on_button("3")
        gui_app._on_button("←")
        gui_app._on_button("4")
        gui_app._on_button("=")
        assert gui_app._display_var.get() == "9"

    def test_gui_decimal_calculation(self, gui_app):
        """Test calculation with decimal point."""
        gui_app._on_button("2")
        gui_app._on_button(".")
        gui_app._on_button("5")
        gui_app._on_button("+")
        gui_app._on_button("1")
        gui_app._on_button(".")
        gui_app._on_button("5")
        gui_app._on_button("=")
        assert gui_app._display_var.get() == "4.0"


# ============================================================================
# Main Function Tests
# ============================================================================


class TestMainGUIFlag:
    """Tests for --gui flag in main.py."""

    @patch("sys.argv", ["script.py", "--gui"])
    @patch("src.gui.CalculatorGUI")
    def test_main_with_gui_flag(self, mock_gui_class):
        """Test main() recognizes --gui flag and launches GUI."""
        from src.main import main

        mock_instance = MagicMock()
        mock_gui_class.return_value = mock_instance

        main()

        mock_gui_class.assert_called_once()
        mock_instance.mainloop.assert_called_once()

    @patch("sys.argv", ["script.py", "-g"])
    @patch("src.gui.CalculatorGUI")
    def test_main_with_g_flag(self, mock_gui_class):
        """Test main() recognizes -g flag and launches GUI."""
        from src.main import main

        mock_instance = MagicMock()
        mock_gui_class.return_value = mock_instance

        main()

        mock_gui_class.assert_called_once()
        mock_instance.mainloop.assert_called_once()

    @patch("sys.argv", ["script.py", "--gui"])
    @patch("src.gui.CalculatorGUI")
    def test_main_gui_creates_calculator(self, mock_gui_class):
        """Test main() creates Calculator instance for GUI."""
        from src.main import main

        mock_instance = MagicMock()
        mock_gui_class.return_value = mock_instance

        main()

        # Verify CalculatorGUI was called with a Calculator instance
        call_args = mock_gui_class.call_args
        assert call_args is not None
        assert isinstance(call_args[0][0], Calculator)

    @patch("sys.argv", ["script.py", "add 5 3"])
    @patch("builtins.input", side_effect=["exit"])
    def test_main_cli_mode_unchanged(self, mock_input, capsys):
        """Test main() with expression arg still uses CLI mode."""
        from src.main import main

        with pytest.raises(SystemExit):
            main()

        captured = capsys.readouterr()
        # Should show CLI result
        assert "8" in captured.out

    @patch("sys.argv", ["script.py"])
    @patch("builtins.input", side_effect=["exit"])
    def test_main_repl_mode_unchanged(self, mock_input, capsys):
        """Test main() with no args still uses REPL mode."""
        from src.main import main

        main()

        captured = capsys.readouterr()
        # Should show REPL welcome/goodbye
        assert "Goodbye!" in captured.out or "Calculator" in captured.out


# ============================================================================
# Display Helper Tests
# ============================================================================


class TestGUIDisplayHelpers:
    """Tests for display-related helper methods."""

    def test_gui_set_display(self, gui_app):
        """Test _set_display() updates the display variable."""
        gui_app._set_display("Test Text")
        assert gui_app._display_var.get() == "Test Text"

    def test_gui_set_display_empty(self, gui_app):
        """Test _set_display() with empty string."""
        gui_app._set_display("")
        assert gui_app._display_var.get() == ""

    def test_gui_show_error_sets_display(self, gui_app):
        """Test _show_error() displays error message."""
        gui_app._show_error("Test Error Message")
        assert gui_app._display_var.get() == "Test Error Message"

    def test_gui_show_error_logs_warning(self, gui_app):
        """Test _show_error() logs a warning."""
        with patch("src.gui.logger") as mock_logger:
            gui_app._show_error("Test Error")
            mock_logger.warning.assert_called()


# ============================================================================
# Display StringVar Tests
# ============================================================================


class TestGUIDisplayVar:
    """Tests for the display variable initialization and behavior."""

    def test_gui_display_var_initialized_empty(self, gui_app):
        """Test that _display_var is initialized to empty string."""
        assert gui_app._display_var.get() == ""

    def test_gui_display_var_is_stringvar(self, gui_app):
        """Test that _display_var is a tk.StringVar."""
        assert isinstance(gui_app._display_var, tk.StringVar)

    def test_gui_display_var_updates_with_append(self, gui_app):
        """Test that display updates when expression is appended."""
        gui_app._append("5")
        assert gui_app._display_var.get() == "5"

    def test_gui_display_var_synced_with_expression(self, gui_app):
        """Test that display and expression stay synchronized."""
        for i in range(5):
            gui_app._append(str(i))
            assert gui_app._display_var.get() == gui_app._expression
