"""test_gui.py — comprehensive tests for the CalculatorGUI module.

Tests the CalculatorGUI class and the --gui flag in main.py.
Uses mocking to work in headless CI without tkinter.
"""

import pytest
import sys
from unittest.mock import patch, MagicMock, call, Mock, ANY
import importlib.util

from src.calculator import Calculator
from src.input_handler import ExpressionParser, InputValidator, OperationNotAvailableInModeError


# ============================================================================
# CRITICAL: Mock tkinter BEFORE any import of src.gui
# ============================================================================
# This mocking must happen at module load time, before src.gui is imported,
# to prevent the real tkinter from being loaded (which would fail in CI).

class MockStringVar:
    """Mock tk.StringVar for storing and retrieving string values."""
    def __init__(self, value=""):
        self._value = value
        self._trace_callbacks = []

    def set(self, value):
        self._value = value
        for callback in self._trace_callbacks:
            callback(self._value)

    def get(self):
        return self._value

    def trace_add(self, mode, callback):
        """Mock trace_add to register callbacks."""
        if mode == "write":
            self._trace_callbacks.append(callback)
        return "dummy_id"

    def trace_remove(self, mode, variable, callback):
        """Mock trace_remove."""
        pass


class MockWidget:
    """Base mock widget supporting all necessary tkinter widget methods."""
    def __init__(self, *args, **kwargs):
        self._grid_info = {}
        self._config = {}
        self._text = kwargs.get("text", "")
        self._is_removed = False

    def grid(self, **kwargs):
        """Mock grid layout manager."""
        self._grid_info = kwargs
        self._is_removed = False

    def grid_remove(self):
        """Mock grid_remove to hide widget."""
        self._is_removed = True

    def grid_forget(self):
        """Mock grid_forget."""
        self._grid_info = {}

    def pack(self, **kwargs):
        """Mock pack layout manager."""
        pass

    def withdraw(self):
        """Mock withdraw (for Tk root window)."""
        pass

    def destroy(self):
        """Mock destroy."""
        pass

    def config(self, **kwargs):
        """Mock config method."""
        self._config.update(kwargs)

    def configure(self, **kwargs):
        """Mock configure method (alias for config)."""
        self._config.update(kwargs)

    def delete(self, *args):
        """Mock delete for Entry widgets."""
        pass

    def insert(self, *args):
        """Mock insert for Entry widgets."""
        pass

    def get(self):
        """Mock get for Entry widgets and StringVar."""
        if isinstance(self, MockStringVar):
            return self._value
        return ""

    def cget(self, key):
        """Mock cget to retrieve config values."""
        return self._config.get(key)


class MockTk(MockWidget):
    """Mock tk.Tk root window."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._title = "Calculator"
        self._resizable_w = False
        self._resizable_h = False

    def title(self, text=None):
        """Get or set window title."""
        if text is None:
            return self._title
        self._title = text

    def resizable(self, width=None, height=None):
        """Get or set window resizability."""
        if width is None:
            return (self._resizable_w, self._resizable_h)
        self._resizable_w = width
        self._resizable_h = height

    def columnconfigure(self, *args, **kwargs):
        """Mock columnconfigure."""
        pass

    def rowconfigure(self, *args, **kwargs):
        """Mock rowconfigure."""
        pass

    def mainloop(self):
        """Mock mainloop."""
        pass


class MockButton(MockWidget):
    """Mock tk.Button widget."""
    def __init__(self, parent=None, **kwargs):
        super().__init__(**kwargs)
        self._command = kwargs.get("command")
        self._text = kwargs.get("text", "")

    def invoke(self):
        """Invoke the button's command."""
        if self._command:
            self._command()


class MockEntry(MockWidget):
    """Mock tk.Entry widget."""
    def __init__(self, parent=None, **kwargs):
        super().__init__(**kwargs)
        self._value = ""
        if "textvariable" in kwargs:
            self._textvariable = kwargs["textvariable"]
        else:
            self._textvariable = None


class MockFrame(MockWidget):
    """Mock tk.Frame widget."""
    def __init__(self, parent=None, **kwargs):
        super().__init__(**kwargs)


class MockLabel(MockWidget):
    """Mock tk.Label widget."""
    def __init__(self, parent=None, **kwargs):
        super().__init__(**kwargs)
        self._text = kwargs.get("text", "")


class MockOptionMenu(MockWidget):
    """Mock tk.OptionMenu widget."""
    def __init__(self, parent, variable, *values, **kwargs):
        super().__init__(**kwargs)
        self._variable = variable
        self._values = values
        self._command = kwargs.get("command")


# Create the mock tkinter module and inject it into sys.modules BEFORE any imports
mock_tkinter = MagicMock()
mock_tkinter.Tk = MockTk
mock_tkinter.StringVar = MockStringVar
mock_tkinter.Entry = MockEntry
mock_tkinter.Frame = MockFrame
mock_tkinter.Label = MockLabel
mock_tkinter.Button = MockButton
mock_tkinter.OptionMenu = MockOptionMenu
mock_tkinter.END = "end"
mock_tkinter.DISABLED = "disabled"
mock_tkinter.NORMAL = "normal"

# Inject the mock BEFORE importing src.gui
sys.modules["tkinter"] = mock_tkinter

# Now we can safely import tkinter and src.gui
import tkinter as tk
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


# ============================================================================
# Button Layout and Mode Switching Tests
# ============================================================================


class TestGUIButtonWidgetStorage:
    """Tests for button widget storage and initialization."""

    def test_gui_button_widgets_initialized(self, gui_app):
        """Test that _button_widgets dict is populated after initialization."""
        assert gui_app._button_widgets is not None
        assert isinstance(gui_app._button_widgets, dict)
        assert len(gui_app._button_widgets) > 0

    def test_gui_button_widgets_contains_basic_labels(self, gui_app):
        """Test that basic mode buttons are in _button_widgets."""
        basic_labels = {"C", "←", "=", "7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "0", ".", "+"}
        for label in basic_labels:
            assert label in gui_app._button_widgets, f"Button '{label}' not found in _button_widgets"

    def test_gui_button_widgets_contains_advanced_labels(self, gui_app):
        """Test that advanced mode buttons are in _button_widgets."""
        advanced_labels = {"x²", "x³", "√", "∛", "xⁿ", "n!", "ln", "log"}
        for label in advanced_labels:
            assert label in gui_app._button_widgets, f"Button '{label}' not found in _button_widgets"

    def test_gui_button_widgets_contains_scientific_labels(self, gui_app):
        """Test that scientific mode buttons are in _button_widgets."""
        scientific_labels = {"sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "exp", "deg", "rad"}
        for label in scientific_labels:
            assert label in gui_app._button_widgets, f"Button '{label}' not found in _button_widgets"

    def test_gui_button_grid_kwargs_populated(self, gui_app):
        """Test that _button_grid_kwargs contains grid info for all buttons."""
        assert hasattr(gui_app, "_button_grid_kwargs")
        assert isinstance(gui_app._button_grid_kwargs, dict)
        assert len(gui_app._button_grid_kwargs) > 0


class TestGUIInitialModeButtonVisibility:
    """Tests for button visibility in initial mode."""

    def test_gui_basic_mode_initial_buttons_visible(self, calculator):
        """Test that basic buttons are visible when starting in basic mode."""
        calculator.set_mode("basic")
        app = CalculatorGUI(calculator)
        basic_labels = {"C", "←", "=", "7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "0", ".", "+"}
        for label in basic_labels:
            btn = app._button_widgets[label]
            assert not btn._is_removed, f"Button '{label}' should be visible in basic mode"

    def test_gui_basic_mode_advanced_buttons_hidden(self, calculator):
        """Test that advanced buttons are hidden when starting in basic mode."""
        calculator.set_mode("basic")
        app = CalculatorGUI(calculator)
        advanced_labels = {"x²", "x³", "√", "∛", "xⁿ", "n!", "ln", "log"}
        for label in advanced_labels:
            btn = app._button_widgets[label]
            assert btn._is_removed, f"Button '{label}' should be hidden in basic mode"

    def test_gui_advanced_mode_initial_buttons_visible(self, calculator):
        """Test that basic and advanced buttons are visible when starting in advanced mode."""
        calculator.set_mode("advanced")
        app = CalculatorGUI(calculator)
        visible_labels = {"C", "←", "=", "7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "0", ".", "+",
                         "x²", "x³", "√", "∛", "xⁿ", "n!", "ln", "log"}
        for label in visible_labels:
            btn = app._button_widgets[label]
            assert not btn._is_removed, f"Button '{label}' should be visible in advanced mode"

    def test_gui_advanced_mode_scientific_buttons_hidden(self, calculator):
        """Test that scientific buttons are hidden when starting in advanced mode."""
        calculator.set_mode("advanced")
        app = CalculatorGUI(calculator)
        scientific_labels = {"sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "exp", "deg", "rad"}
        for label in scientific_labels:
            btn = app._button_widgets[label]
            assert btn._is_removed, f"Button '{label}' should be hidden in advanced mode"

    def test_gui_scientific_mode_all_buttons_visible(self, calculator):
        """Test that all buttons are visible when starting in scientific mode."""
        calculator.set_mode("scientific")
        app = CalculatorGUI(calculator)
        all_labels = {"C", "←", "=", "7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "0", ".", "+",
                      "x²", "x³", "√", "∛", "xⁿ", "n!", "ln", "log",
                      "sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "exp", "deg", "rad"}
        for label in all_labels:
            btn = app._button_widgets[label]
            assert not btn._is_removed, f"Button '{label}' should be visible in scientific mode"


class TestGUIRebuildButtonGridForMode:
    """Tests for _rebuild_button_grid_for_mode() method."""

    def test_rebuild_button_grid_to_basic(self, gui_app):
        """Test rebuilding button grid to basic mode."""
        gui_app._calculator.set_mode("scientific")
        gui_app._rebuild_button_grid_for_mode("basic")

        basic_labels = {"C", "←", "=", "7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "0", ".", "+"}
        advanced_labels = {"x²", "x³", "√", "∛", "xⁿ", "n!", "ln", "log"}
        scientific_labels = {"sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "exp", "deg", "rad"}

        for label in basic_labels:
            assert not gui_app._button_widgets[label]._is_removed, f"Button '{label}' should be visible in basic mode"

        for label in advanced_labels | scientific_labels:
            assert gui_app._button_widgets[label]._is_removed, f"Button '{label}' should be hidden in basic mode"

    def test_rebuild_button_grid_to_advanced(self, gui_app):
        """Test rebuilding button grid to advanced mode."""
        gui_app._calculator.set_mode("basic")
        gui_app._rebuild_button_grid_for_mode("advanced")

        basic_labels = {"C", "←", "=", "7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "0", ".", "+"}
        advanced_labels = {"x²", "x³", "√", "∛", "xⁿ", "n!", "ln", "log"}
        scientific_labels = {"sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "exp", "deg", "rad"}

        for label in basic_labels | advanced_labels:
            assert not gui_app._button_widgets[label]._is_removed, f"Button '{label}' should be visible in advanced mode"

        for label in scientific_labels:
            assert gui_app._button_widgets[label]._is_removed, f"Button '{label}' should be hidden in advanced mode"

    def test_rebuild_button_grid_to_scientific(self, gui_app):
        """Test rebuilding button grid to scientific mode."""
        gui_app._calculator.set_mode("basic")
        gui_app._rebuild_button_grid_for_mode("scientific")

        all_labels = {"C", "←", "=", "7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "0", ".", "+",
                      "x²", "x³", "√", "∛", "xⁿ", "n!", "ln", "log",
                      "sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "exp", "deg", "rad"}

        for label in all_labels:
            assert not gui_app._button_widgets[label]._is_removed, f"Button '{label}' should be visible in scientific mode"

    def test_rebuild_button_grid_unknown_mode_falls_back_to_basic(self, gui_app):
        """Test that unknown mode falls back to basic."""
        gui_app._calculator.set_mode("scientific")
        gui_app._rebuild_button_grid_for_mode("unknown_mode")

        basic_labels = {"C", "←", "=", "7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "0", ".", "+"}
        advanced_labels = {"x²", "x³", "√", "∛", "xⁿ", "n!", "ln", "log"}
        scientific_labels = {"sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "exp", "deg", "rad"}

        for label in basic_labels:
            assert not gui_app._button_widgets[label]._is_removed, f"Button '{label}' should be visible after fallback"

        for label in advanced_labels | scientific_labels:
            assert gui_app._button_widgets[label]._is_removed, f"Button '{label}' should be hidden after fallback"

    def test_rebuild_button_grid_calls_grid_on_visible_buttons(self, gui_app):
        """Test that grid() is called with correct kwargs for visible buttons."""
        gui_app._rebuild_button_grid_for_mode("basic")

        basic_labels = {"C", "←", "=", "7", "8"}
        for label in basic_labels:
            btn = gui_app._button_widgets[label]
            grid_kwargs = gui_app._button_grid_kwargs[label]
            assert btn._grid_info == grid_kwargs, f"Button '{label}' grid_info should match stored kwargs"

    def test_rebuild_button_grid_calls_grid_remove_on_hidden_buttons(self, gui_app):
        """Test that grid_remove() is called for hidden buttons."""
        gui_app._rebuild_button_grid_for_mode("basic")

        advanced_labels = {"x²", "x³", "√", "∛"}
        for label in advanced_labels:
            btn = gui_app._button_widgets[label]
            assert btn._is_removed, f"Button '{label}' should be removed from grid"


class TestGUIModeChangeTriggersRebuild:
    """Tests for mode change triggering button grid rebuild."""

    def test_on_mode_change_calls_rebuild_basic_to_advanced(self, gui_app):
        """Test that _on_mode_change triggers rebuild when switching to advanced."""
        gui_app._calculator.set_mode("basic")
        gui_app._on_mode_change("advanced")

        advanced_labels = {"x²", "x³", "√", "∛", "xⁿ", "n!", "ln", "log"}
        for label in advanced_labels:
            assert not gui_app._button_widgets[label]._is_removed, f"Button '{label}' should be visible after mode change"

    def test_on_mode_change_calls_rebuild_advanced_to_scientific(self, gui_app):
        """Test that _on_mode_change triggers rebuild when switching to scientific."""
        gui_app._calculator.set_mode("advanced")
        gui_app._on_mode_change("scientific")

        scientific_labels = {"sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "exp", "deg", "rad"}
        for label in scientific_labels:
            assert not gui_app._button_widgets[label]._is_removed, f"Button '{label}' should be visible after mode change"

    def test_on_mode_change_calls_rebuild_scientific_to_basic(self, gui_app):
        """Test that _on_mode_change triggers rebuild when switching to basic."""
        gui_app._calculator.set_mode("scientific")
        gui_app._on_mode_change("basic")

        advanced_labels = {"x²", "x³", "√", "∛", "xⁿ", "n!", "ln", "log"}
        scientific_labels = {"sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "exp", "deg", "rad"}

        for label in advanced_labels | scientific_labels:
            assert gui_app._button_widgets[label]._is_removed, f"Button '{label}' should be hidden after mode change"

    def test_on_mode_change_with_invalid_mode_does_not_rebuild(self, gui_app):
        """Test that invalid mode does not trigger rebuild."""
        gui_app._calculator.set_mode("basic")
        initial_state = {label: btn._is_removed for label, btn in gui_app._button_widgets.items()}

        gui_app._on_mode_change("invalid_mode")

        final_state = {label: btn._is_removed for label, btn in gui_app._button_widgets.items()}
        assert initial_state == final_state, "Button visibility should not change on invalid mode"

    def test_on_mode_change_invalid_mode_shows_error(self, gui_app):
        """Test that invalid mode change shows error message."""
        gui_app._on_mode_change("invalid_mode")
        display = gui_app._display_var.get()
        assert display.startswith("Mode error:")


class TestGUIAppendFunction:
    """Tests for _append_function() method."""

    @pytest.mark.parametrize("label,operation", [
        ("x²", "square"),
        ("x³", "cube"),
        ("√", "square_root"),
        ("∛", "cube_root"),
        ("xⁿ", "power"),
        ("n!", "factorial"),
        ("ln", "natural_log"),
        ("log", "log_base_10"),
        ("sin", "sin"),
        ("cos", "cos"),
        ("tan", "tan"),
        ("asin", "asin"),
        ("acos", "acos"),
        ("atan", "atan"),
        ("sinh", "sinh"),
        ("cosh", "cosh"),
        ("tanh", "tanh"),
        ("exp", "exp"),
        ("deg", "degrees"),
        ("rad", "radians"),
    ])
    def test_append_function_empty_expression(self, gui_app, label, operation):
        """Test _append_function on empty expression starts operation."""
        gui_app._expression = ""
        gui_app._append_function(label)
        assert gui_app._expression == operation + " ", f"Expression should be '{operation} ' but got '{gui_app._expression}'"

    @pytest.mark.parametrize("label,operation", [
        ("x²", "square"),
        ("√", "square_root"),
        ("sin", "sin"),
        ("exp", "exp"),
    ])
    def test_append_function_with_number(self, gui_app, label, operation):
        """Test _append_function with typed number treats it as operand."""
        gui_app._expression = "4"
        gui_app._append_function(label)
        assert gui_app._expression == operation + " 4 ", f"Expression should be '{operation} 4 ' but got '{gui_app._expression}'"

    @pytest.mark.parametrize("label", ["x²", "√", "sin", "exp", "deg"])
    def test_append_function_display_updated(self, gui_app, label):
        """Test _append_function updates the display."""
        gui_app._append_function(label)
        assert gui_app._display_var.get() == gui_app._expression


class TestGUIOnButtonDispatchesFunction:
    """Tests for _on_button() dispatching to _append_function()."""

    @pytest.mark.parametrize("label", ["x²", "x³", "√", "∛", "xⁿ", "n!", "ln", "log", "sin", "cos", "tan", "exp", "deg", "rad"])
    def test_on_button_dispatches_function_button_empty_expr(self, gui_app, label):
        """Test that _on_button dispatches function buttons correctly."""
        gui_app._on_button(label)
        # Verify that the operation was set in the expression
        assert gui_app._expression != "", f"Expression should not be empty after pressing '{label}'"
        # Verify that it's a valid operation (starts with operation name)
        from src.gui import _LABEL_TO_OPERATION
        operation = _LABEL_TO_OPERATION[label]
        assert gui_app._expression.startswith(operation), f"Expression should start with '{operation}' but got '{gui_app._expression}'"

    def test_on_button_function_with_operand(self, gui_app):
        """Test _on_button with function button when operand exists."""
        gui_app._append("5")
        gui_app._on_button("x²")
        assert gui_app._expression == "square 5 "

    def test_on_button_chain_function_calls(self, gui_app):
        """Test chaining function button presses."""
        gui_app._append("16")
        gui_app._on_button("√")
        assert "square_root" in gui_app._expression


class TestGUIEndToEndButtonAndEvaluate:
    """End-to-end tests for button presses and evaluation."""

    def test_end_to_end_square_function(self, gui_app):
        """Test complete flow: press 4, press x², press =, expect 16."""
        gui_app._on_button("4")
        assert gui_app._expression == "4"

        gui_app._on_button("x²")
        assert gui_app._expression == "square 4 "

        gui_app._on_button("=")
        assert gui_app._display_var.get() == "16"
        assert gui_app._expression == "16"

    def test_end_to_end_square_root(self, gui_app):
        """Test complete flow: press 16, press √, press =, expect 4."""
        gui_app._on_button("1")
        gui_app._on_button("6")
        assert gui_app._expression == "16"

        gui_app._on_button("√")
        assert gui_app._expression == "square_root 16 "

        gui_app._on_button("=")
        assert gui_app._display_var.get() == "4.0"

    def test_end_to_end_factorial(self, gui_app):
        """Test factorial: press 5, press n!, press =, expect 120."""
        gui_app._on_button("5")
        gui_app._on_button("n!")
        assert gui_app._expression == "factorial 5 "

        gui_app._on_button("=")
        assert gui_app._display_var.get() == "120"

    def test_end_to_end_result_chain_with_function(self, gui_app):
        """Test chaining: 4 + 5 =, then press x², =, expect 81."""
        gui_app._append("4")
        gui_app._append_operator("+")
        gui_app._append("5")
        gui_app._on_button("=")
        assert gui_app._expression == "9"

        gui_app._on_button("x²")
        assert gui_app._expression == "square 9 "

        gui_app._on_button("=")
        assert gui_app._display_var.get() == "81"
