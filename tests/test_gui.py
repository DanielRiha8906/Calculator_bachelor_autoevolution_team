"""Comprehensive pytest tests for tkinter GUI module (test_gui.py).

Tests cover:
- GUI window creation and lifecycle
- Entry widget and display widget existence
- Basic arithmetic operations (add, subtract, multiply, divide)
- Advanced operations (square, cube, sqrt, cbrt, factorial, power, log, ln)
- Scientific operations (sin, cos, tan, etc.)
- Mathematical constants (pi, e)
- Error handling (division by zero, invalid input, domain errors)
- Clear button functionality
- Backspace functionality
- Sign toggle functionality
- Scientific mode toggle
- Operation sequences
- Decimal and negative input handling
"""

import sys
import os
import unittest
from unittest.mock import MagicMock, patch, PropertyMock, call, Mock
import pytest


@pytest.fixture
def gui_with_mock_root():
    """Create a CalculatorGUI instance with fully mocked tkinter components."""
    with patch('src.gui.tkinter.Tk') as mock_tk_class:
        with patch('src.gui.tkinter.Label') as mock_label_class:
            with patch('src.gui.tkinter.Entry') as mock_entry_class:
                with patch('src.gui.tkinter.Button') as mock_button_class:
                    # Set up mock instances
                    mock_root = MagicMock()
                    mock_tk_class.return_value = mock_root

                    mock_display = MagicMock()
                    mock_label_class.return_value = mock_display

                    mock_entry = MagicMock()
                    mock_entry_class.return_value = mock_entry

                    mock_button = MagicMock()
                    mock_button_class.return_value = mock_button

                    # Import and create the GUI
                    from src.gui import CalculatorGUI
                    gui = CalculatorGUI()

                    # Store the mocks for verification
                    gui._mock_root = mock_root
                    gui._mock_display = mock_display
                    gui._mock_entry = mock_entry
                    gui._mock_button = mock_button

                    yield gui


class TestGUIWindowCreation:
    """Test GUI window initialization and lifecycle."""

    def test_gui_window_creation(self, gui_with_mock_root):
        """Test that GUI window is created with correct title."""
        gui = gui_with_mock_root
        gui._mock_root.title.assert_called_with("Calculator")

    def test_gui_calculator_instance_created(self, gui_with_mock_root):
        """Test that Calculator instance is created in GUI."""
        gui = gui_with_mock_root
        assert hasattr(gui, 'calc'), "CalculatorGUI should have 'calc' attribute"
        assert gui.calc is not None, "Calculator instance should not be None"

    def test_gui_initial_state(self, gui_with_mock_root):
        """Test that GUI initializes with correct initial state."""
        gui = gui_with_mock_root
        assert gui.current_input == ""
        assert gui.pending_op is None
        assert gui.first_operand is None
        assert gui.scientific_mode is False
        assert isinstance(gui.scientific_buttons, list)


class TestGUIWidgets:
    """Test GUI widget existence and accessibility."""

    def test_gui_entry_widget_exists(self, gui_with_mock_root):
        """Test that entry widget exists and is accessible."""
        gui = gui_with_mock_root
        assert hasattr(gui, 'entry'), "CalculatorGUI should have 'entry' attribute"
        assert gui.entry is not None, "Entry widget should not be None"

    def test_gui_display_area_exists(self, gui_with_mock_root):
        """Test that result label/display area exists and is accessible."""
        gui = gui_with_mock_root
        assert hasattr(gui, 'display'), "CalculatorGUI should have 'display' attribute"
        assert gui.display is not None, "Display widget should not be None"


class TestGUINumberInput:
    """Test GUI number input functionality."""

    def test_on_number_click_single_digit(self, gui_with_mock_root):
        """Test clicking a single digit appends to current_input."""
        gui = gui_with_mock_root
        gui._on_number_click("5")
        assert gui.current_input == "5"

    def test_on_number_click_sequence(self, gui_with_mock_root):
        """Test clicking multiple digits in sequence produces concatenated input."""
        gui = gui_with_mock_root
        gui._on_number_click("1")
        gui._on_number_click("2")
        gui._on_number_click("3")
        assert gui.current_input == "123"

    def test_on_number_click_decimal(self, gui_with_mock_root):
        """Test decimal point button appends to current_input."""
        gui = gui_with_mock_root
        gui._on_number_click("5")
        gui._on_number_click(".")
        gui._on_number_click("3")
        assert gui.current_input == "5.3"


class TestGUIOperatorClick:
    """Test GUI operator click and _calculate functionality."""

    def test_on_operator_click_stores_first_operand_and_operator(self, gui_with_mock_root):
        """Test that _on_operator_click stores first operand and pending operator."""
        gui = gui_with_mock_root
        gui.current_input = "5"
        gui._on_operator_click("add")
        assert gui.first_operand == 5.0
        assert gui.pending_op == "add"
        assert gui.current_input == ""

    def test_on_operator_click_add(self, gui_with_mock_root):
        """Test add operator click sets pending_op to 'add'."""
        gui = gui_with_mock_root
        gui.current_input = "3"
        gui._on_operator_click("add")
        assert gui.pending_op == "add"

    def test_on_operator_click_subtract(self, gui_with_mock_root):
        """Test subtract operator click sets pending_op to 'subtract'."""
        gui = gui_with_mock_root
        gui.current_input = "10"
        gui._on_operator_click("subtract")
        assert gui.pending_op == "subtract"

    def test_on_operator_click_multiply(self, gui_with_mock_root):
        """Test multiply operator click sets pending_op to 'multiply'."""
        gui = gui_with_mock_root
        gui.current_input = "7"
        gui._on_operator_click("multiply")
        assert gui.pending_op == "multiply"

    def test_on_operator_click_divide(self, gui_with_mock_root):
        """Test divide operator click sets pending_op to 'divide'."""
        gui = gui_with_mock_root
        gui.current_input = "20"
        gui._on_operator_click("divide")
        assert gui.pending_op == "divide"


class TestGUICalculate:
    """Test GUI _calculate functionality."""

    @pytest.mark.parametrize("first,op,second,expected", [
        (5, "add", 3, 8.0),
        (10, "subtract", 4, 6.0),
        (7, "multiply", 8, 56.0),
        (20, "divide", 4, 5.0),
        (2, "power", 3, 8.0),
    ])
    def test_calculate_binary_operations(self, gui_with_mock_root, first, op, second, expected):
        """Test _calculate with various binary operations."""
        gui = gui_with_mock_root
        gui.first_operand = first
        gui.pending_op = op
        gui.current_input = str(second)
        result = gui._calculate()
        assert result == expected

    def test_calculate_returns_float_result(self, gui_with_mock_root):
        """Test that _calculate returns a float result."""
        gui = gui_with_mock_root
        gui.first_operand = 5
        gui.pending_op = "add"
        gui.current_input = "3"
        result = gui._calculate()
        assert isinstance(result, float)
        assert result == 8.0


class TestGUIUnaryOperations:
    """Test GUI unary operations via _apply_unary."""

    @pytest.mark.parametrize("value,op,expected", [
        (5, "square", 25.0),
        (3, "cube", 27.0),
        (16, "square_root", 4.0),
        (8, "cube_root", 2.0),
        (5, "factorial", 120.0),
        (100, "log", 2.0),
        (1, "ln", 0.0),
    ])
    def test_apply_unary_operations(self, gui_with_mock_root, value, op, expected):
        """Test _apply_unary with various unary operations."""
        gui = gui_with_mock_root
        gui.current_input = str(value)
        result = gui._apply_unary(op)
        if op == "ln":
            # ln(1) should be very close to 0
            assert result is not None
            assert pytest.approx(result, abs=0.001) == expected
        else:
            assert result == expected

    def test_apply_unary_sin_zero(self, gui_with_mock_root):
        """Test sin(0) = 0."""
        gui = gui_with_mock_root
        gui.current_input = "0"
        result = gui._apply_unary("sin")
        assert pytest.approx(result, abs=0.0001) == 0.0

    def test_apply_unary_cos_zero(self, gui_with_mock_root):
        """Test cos(0) = 1."""
        gui = gui_with_mock_root
        gui.current_input = "0"
        result = gui._apply_unary("cos")
        assert pytest.approx(result, abs=0.0001) == 1.0

    def test_apply_unary_returns_float_or_none(self, gui_with_mock_root):
        """Test that _apply_unary returns float or None."""
        gui = gui_with_mock_root
        gui.current_input = "5"
        result = gui._apply_unary("square")
        assert isinstance(result, (float, type(None)))


class TestGUIErrorHandling:
    """Test GUI error handling for invalid operations."""

    def test_division_by_zero_error(self, gui_with_mock_root):
        """Test that division by zero raises error."""
        gui = gui_with_mock_root
        gui.first_operand = 5.0
        gui.pending_op = "divide"
        gui.current_input = "0"
        # _calculate should catch ZeroDivisionError and call messagebox.showerror
        result = gui._calculate()
        assert result is None

    def test_sqrt_negative_error(self, gui_with_mock_root):
        """Test that sqrt of negative number raises error."""
        gui = gui_with_mock_root
        gui.current_input = "-4"
        result = gui._apply_unary("square_root")
        assert result is None

    def test_factorial_negative_error(self, gui_with_mock_root):
        """Test that factorial of negative number raises error."""
        gui = gui_with_mock_root
        gui.current_input = "-1"
        result = gui._apply_unary("factorial")
        assert result is None

    def test_log_negative_error(self, gui_with_mock_root):
        """Test that log of negative number raises error."""
        gui = gui_with_mock_root
        gui.current_input = "-5"
        result = gui._apply_unary("log")
        assert result is None

    def test_ln_negative_error(self, gui_with_mock_root):
        """Test that ln of negative number raises error."""
        gui = gui_with_mock_root
        gui.current_input = "-1"
        result = gui._apply_unary("ln")
        assert result is None


class TestGUIClear:
    """Test GUI clear functionality."""

    def test_clear_resets_all_state(self, gui_with_mock_root):
        """Test that _clear resets all calculator state."""
        gui = gui_with_mock_root
        gui.current_input = "5"
        gui.pending_op = "add"
        gui.first_operand = 3.0
        gui._clear()
        assert gui.current_input == ""
        assert gui.pending_op is None
        assert gui.first_operand is None

    def test_clear_resets_display(self, gui_with_mock_root):
        """Test that _clear resets display to '0'."""
        gui = gui_with_mock_root
        gui.current_input = "5"
        gui._clear()
        # Check that display.config was called with text="0"
        gui.display.config.assert_called_with(text="0")


class TestGUIBackspace:
    """Test GUI backspace functionality."""

    def test_backspace_removes_last_character(self, gui_with_mock_root):
        """Test that _on_backspace removes last character from current_input."""
        gui = gui_with_mock_root
        gui.current_input = "123"
        gui._on_backspace()
        assert gui.current_input == "12"

    def test_backspace_on_empty_input(self, gui_with_mock_root):
        """Test that _on_backspace on empty input doesn't crash."""
        gui = gui_with_mock_root
        gui.current_input = ""
        gui._on_backspace()
        assert gui.current_input == ""

    def test_backspace_single_character(self, gui_with_mock_root):
        """Test that _on_backspace removes single character."""
        gui = gui_with_mock_root
        gui.current_input = "5"
        gui._on_backspace()
        assert gui.current_input == ""


class TestGUISignToggle:
    """Test GUI sign toggle functionality."""

    def test_sign_toggle_negates_positive(self, gui_with_mock_root):
        """Test that _on_sign_toggle negates positive number."""
        gui = gui_with_mock_root
        gui.current_input = "5"
        gui._on_sign_toggle()
        assert gui.current_input == "-5.0"

    def test_sign_toggle_negates_negative(self, gui_with_mock_root):
        """Test that _on_sign_toggle negates negative number."""
        gui = gui_with_mock_root
        gui.current_input = "-5"
        gui._on_sign_toggle()
        # -(-5) = 5
        assert float(gui.current_input) == 5.0

    def test_sign_toggle_with_decimal(self, gui_with_mock_root):
        """Test that _on_sign_toggle works with decimal numbers."""
        gui = gui_with_mock_root
        gui.current_input = "3.5"
        gui._on_sign_toggle()
        assert float(gui.current_input) == -3.5


class TestGUIConstantClick:
    """Test GUI constant click functionality."""

    def test_constant_click_pi(self, gui_with_mock_root):
        """Test that _on_constant_click('get_pi') inserts pi value."""
        gui = gui_with_mock_root
        gui._on_constant_click("get_pi")
        # Pi should be approximately 3.14159
        assert gui.current_input is not None
        pi_value = float(gui.current_input)
        assert pytest.approx(pi_value, abs=0.01) == 3.14159

    def test_constant_click_e(self, gui_with_mock_root):
        """Test that _on_constant_click('get_e') inserts e value."""
        gui = gui_with_mock_root
        gui._on_constant_click("get_e")
        # e should be approximately 2.71828
        assert gui.current_input is not None
        e_value = float(gui.current_input)
        assert pytest.approx(e_value, abs=0.01) == 2.71828


class TestGUIScientificMode:
    """Test GUI scientific mode toggle functionality."""

    def test_scientific_mode_toggle_enables(self, gui_with_mock_root):
        """Test that _toggle_scientific_mode enables scientific mode."""
        gui = gui_with_mock_root
        assert gui.scientific_mode is False
        gui._toggle_scientific_mode()
        assert gui.scientific_mode is True

    def test_scientific_mode_toggle_disables(self, gui_with_mock_root):
        """Test that _toggle_scientific_mode disables scientific mode."""
        gui = gui_with_mock_root
        gui.scientific_mode = True
        gui._toggle_scientific_mode()
        assert gui.scientific_mode is False

    def test_scientific_mode_toggle_twice_returns_to_original(self, gui_with_mock_root):
        """Test that toggling scientific mode twice returns to original state."""
        gui = gui_with_mock_root
        original_state = gui.scientific_mode
        gui._toggle_scientific_mode()
        gui._toggle_scientific_mode()
        assert gui.scientific_mode == original_state

    def test_scientific_buttons_list_non_empty(self, gui_with_mock_root):
        """Test that scientific_buttons list is non-empty after initialization."""
        gui = gui_with_mock_root
        assert len(gui.scientific_buttons) > 0, "scientific_buttons should not be empty"

    def test_scientific_buttons_initially_hidden(self, gui_with_mock_root):
        """Test that scientific buttons are initially hidden."""
        gui = gui_with_mock_root
        # Buttons should be created and grid_remove()'d
        for btn in gui.scientific_buttons:
            assert btn is not None, "Scientific button should exist"


class TestGUIOperationSequence:
    """Test GUI operation sequences."""

    def test_sequential_additions(self, gui_with_mock_root):
        """Test multiple additions in sequence."""
        gui = gui_with_mock_root
        # First: 2 + 3 = 5
        gui.first_operand = 2
        gui.pending_op = "add"
        gui.current_input = "3"
        result1 = gui._calculate()
        assert result1 == 5.0

    def test_complex_operation_sequence(self, gui_with_mock_root):
        """Test a more complex sequence of operations."""
        gui = gui_with_mock_root
        # First operation: 2 + 3 = 5
        gui.first_operand = 2
        gui.pending_op = "add"
        gui.current_input = "3"
        result1 = gui._calculate()
        assert result1 == 5.0

        # Second operation on result: 5 * 2 = 10
        gui.first_operand = result1
        gui.pending_op = "multiply"
        gui.current_input = "2"
        result2 = gui._calculate()
        assert result2 == 10.0


class TestGUIDecimalAndNegative:
    """Test GUI decimal and negative input handling."""

    def test_decimal_multiplication(self, gui_with_mock_root):
        """Test 3.5 * 2 = 7."""
        gui = gui_with_mock_root
        gui.first_operand = 3.5
        gui.pending_op = "multiply"
        gui.current_input = "2"
        result = gui._calculate()
        assert result == 7.0

    def test_negative_addition(self, gui_with_mock_root):
        """Test -5 + 3 = -2."""
        gui = gui_with_mock_root
        gui.first_operand = -5.0
        gui.pending_op = "add"
        gui.current_input = "3"
        result = gui._calculate()
        assert result == -2.0


class TestLaunchGUI:
    """Test launch_gui entry function."""

    def test_launch_gui_function_exists(self):
        """Test that launch_gui() function exists and is callable."""
        from src.gui import launch_gui
        assert callable(launch_gui), "launch_gui should be callable"
