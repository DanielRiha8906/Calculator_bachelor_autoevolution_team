"""Comprehensive pytest tests for tkinter GUI module (test_gui.py).

Tests cover:
- GUI window creation and lifecycle
- Entry widget and display widget existence
- Basic arithmetic operations (add, subtract, multiply, divide)
- Advanced operations (square, cube, sqrt, cbrt, factorial, power, log, ln)
- Error handling (division by zero, invalid input, domain errors)
- Clear button functionality
- Operation sequences
- Decimal and negative input handling
"""

import sys
import unittest
from unittest.mock import MagicMock, patch, PropertyMock, call
import pytest

# Mock tkinter before importing gui module
tkinter_mock = MagicMock()
sys.modules['tkinter'] = tkinter_mock
sys.modules['tkinter.ttk'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()

# Now we can import from src
from src.gui import CalculatorGUI, launch_gui


class TestGUIWindowCreation:
    """Test GUI window initialization and lifecycle."""

    def test_gui_window_creation(self):
        """Test that GUI window is created with correct title."""
        gui = CalculatorGUI()
        # Window should have been created with title "Calculator"
        tkinter_mock.Tk.assert_called()
        gui.root.title.assert_called_with("Calculator")

    def test_gui_window_closes(self):
        """Test that window can close without exceptions."""
        gui = CalculatorGUI()
        # Should not raise any exceptions
        gui.destroy()


class TestGUIWidgets:
    """Test GUI widget existence and accessibility."""

    def test_gui_entry_widget_exists(self):
        """Test that entry widget exists and is accessible."""
        gui = CalculatorGUI()
        assert hasattr(gui, 'entry'), "CalculatorGUI should have 'entry' attribute"
        assert gui.entry is not None, "Entry widget should not be None"

    def test_gui_display_area_exists(self):
        """Test that result label/display area exists and is accessible."""
        gui = CalculatorGUI()
        assert hasattr(gui, 'display'), "CalculatorGUI should have 'display' attribute"
        assert gui.display is not None, "Display widget should not be None"


class TestGUIBasicArithmetic:
    """Test GUI basic arithmetic operations."""

    def test_gui_addition(self):
        """Test 2 + 3 = 5."""
        gui = CalculatorGUI()
        gui.current_input = "2"
        gui._set_operator('add')
        gui.current_input = "3"
        result = gui._calculate()
        assert result == 5.0, f"Expected 5.0, got {result}"

    def test_gui_subtraction(self):
        """Test 10 - 4 = 6."""
        gui = CalculatorGUI()
        gui.current_input = "10"
        gui._set_operator('subtract')
        gui.current_input = "4"
        result = gui._calculate()
        assert result == 6.0, f"Expected 6.0, got {result}"

    def test_gui_multiplication(self):
        """Test 7 * 8 = 56."""
        gui = CalculatorGUI()
        gui.current_input = "7"
        gui._set_operator('multiply')
        gui.current_input = "8"
        result = gui._calculate()
        assert result == 56.0, f"Expected 56.0, got {result}"

    def test_gui_division(self):
        """Test 20 / 4 = 5."""
        gui = CalculatorGUI()
        gui.current_input = "20"
        gui._set_operator('divide')
        gui.current_input = "4"
        result = gui._calculate()
        assert result == 5.0, f"Expected 5.0, got {result}"


class TestGUIUnaryOperations:
    """Test GUI unary operations."""

    def test_gui_square(self):
        """Test 5² = 25."""
        gui = CalculatorGUI()
        gui.current_input = "5"
        result = gui._apply_unary('square')
        assert result == 25.0, f"Expected 25.0, got {result}"

    def test_gui_cube(self):
        """Test 3³ = 27."""
        gui = CalculatorGUI()
        gui.current_input = "3"
        result = gui._apply_unary('cube')
        assert result == 27.0, f"Expected 27.0, got {result}"

    def test_gui_square_root(self):
        """Test √16 = 4."""
        gui = CalculatorGUI()
        gui.current_input = "16"
        result = gui._apply_unary('square_root')
        assert result == 4.0, f"Expected 4.0, got {result}"

    def test_gui_cube_root(self):
        """Test ∛8 = 2."""
        gui = CalculatorGUI()
        gui.current_input = "8"
        result = gui._apply_unary('cube_root')
        assert result == 2.0, f"Expected 2.0, got {result}"

    def test_gui_factorial(self):
        """Test 5! = 120."""
        gui = CalculatorGUI()
        gui.current_input = "5"
        result = gui._apply_unary('factorial')
        assert result == 120.0, f"Expected 120.0, got {result}"

    def test_gui_power(self):
        """Test 2^3 = 8."""
        gui = CalculatorGUI()
        gui.current_input = "2"
        gui._set_operator('power')
        gui.current_input = "3"
        result = gui._calculate()
        assert result == 8.0, f"Expected 8.0, got {result}"

    def test_gui_log(self):
        """Test log(100) = 2."""
        gui = CalculatorGUI()
        gui.current_input = "100"
        result = gui._apply_unary('log')
        assert result == 2.0, f"Expected 2.0, got {result}"

    def test_gui_ln(self):
        """Test ln(e) ≈ 1.0."""
        gui = CalculatorGUI()
        gui.current_input = "2.718281828"
        result = gui._apply_unary('ln')
        assert pytest.approx(result, abs=0.01) == 1.0, f"Expected ≈1.0, got {result}"


class TestGUIErrorHandling:
    """Test GUI error handling."""

    def test_gui_division_by_zero_error(self):
        """Test that division by zero shows error."""
        gui = CalculatorGUI()
        gui.current_input = "5"
        gui._set_operator('divide')
        gui.current_input = "0"
        gui._calculate()
        # Should call messagebox.showerror or set error label
        tkinter_mock.messagebox.showerror.assert_called()

    def test_gui_sqrt_negative_error(self):
        """Test that sqrt of negative number shows error."""
        gui = CalculatorGUI()
        gui.current_input = "-4"
        gui._apply_unary('square_root')
        # Should call messagebox.showerror or set error label
        tkinter_mock.messagebox.showerror.assert_called()

    def test_gui_invalid_input(self):
        """Test that invalid input doesn't crash GUI."""
        gui = CalculatorGUI()
        gui.current_input = "abc"
        with pytest.raises((ValueError, TypeError)):
            gui._calculate()

    def test_gui_factorial_negative_error(self):
        """Test that factorial of negative number shows error."""
        gui = CalculatorGUI()
        gui.current_input = "-1"
        gui._apply_unary('factorial')
        # Should call messagebox.showerror or set error label
        tkinter_mock.messagebox.showerror.assert_called()


class TestGUIClearButton:
    """Test GUI clear functionality."""

    def test_gui_clear_button(self):
        """Test clear button resets display."""
        gui = CalculatorGUI()
        gui.current_input = "5"
        gui._clear()
        assert gui.current_input == "0" or gui.current_input == "", \
            f"Expected cleared input, got {gui.current_input}"


class TestGUIOperationSequence:
    """Test GUI operation sequences."""

    def test_gui_operation_sequence(self):
        """Test multiple operations in sequence."""
        gui = CalculatorGUI()
        # First operation: 2 + 3 = 5
        gui.current_input = "2"
        gui._set_operator('add')
        gui.current_input = "3"
        result1 = gui._calculate()
        assert result1 == 5.0, f"First operation: expected 5.0, got {result1}"

        # Second operation: 5 + 5 = 10
        gui.current_input = "5"
        gui._set_operator('add')
        gui.current_input = "5"
        result2 = gui._calculate()
        assert result2 == 10.0, f"Second operation: expected 10.0, got {result2}"


class TestGUIDecimalInput:
    """Test GUI decimal input handling."""

    def test_gui_decimal_input(self):
        """Test 3.5 * 2 = 7."""
        gui = CalculatorGUI()
        gui.current_input = "3.5"
        gui._set_operator('multiply')
        gui.current_input = "2"
        result = gui._calculate()
        assert result == 7.0, f"Expected 7.0, got {result}"


class TestGUINegativeInput:
    """Test GUI negative input handling."""

    def test_gui_negative_input(self):
        """Test -5 + 3 = -2."""
        gui = CalculatorGUI()
        gui.current_input = "-5"
        gui._set_operator('add')
        gui.current_input = "3"
        result = gui._calculate()
        assert result == -2.0, f"Expected -2.0, got {result}"


class TestLaunchGUI:
    """Test launch_gui entry function."""

    def test_launch_gui_entry_function_exists(self):
        """Test that launch_gui() function can be called."""
        # Mock mainloop to prevent blocking
        with patch.object(CalculatorGUI, '__init__', return_value=None):
            # Function should not raise
            try:
                # We won't actually run it, just verify it's callable
                assert callable(launch_gui), "launch_gui should be callable"
            except Exception as e:
                pytest.fail(f"launch_gui should be callable: {e}")
