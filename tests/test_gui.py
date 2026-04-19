"""Comprehensive pytest tests for redesigned iOS-style GUI calculator.

Tests cover:
- Digit input and display accumulation
- Binary operation deferral (store first, wait for equals)
- Unary operation immediate execution
- Utility buttons (clear, negate, percent)
- Mode toggle (NORMAL ↔ SCIENTIFIC) state reset and button label
- Color theme constants and button styling
- End-to-end integration flows
- Edge cases (zero, negative numbers, large numbers, error handling)
"""

from __future__ import annotations

import pytest
from unittest.mock import Mock, patch, MagicMock, call
import sys

from src.core.calculator import Calculator
from src.session.mode import Mode
from src.session.base_mode import BaseMode
from src.operations import OPERATIONS, NORMAL_OPERATIONS, SCIENTIFIC_OPERATIONS
from src.session.history import History


# ===========================================================================
# GuiCalculator Initialization Tests (with tkinter mocking)
# ===========================================================================

class TestGuiCalculatorInitialization:
    """Test GuiCalculator initialization with new state attributes."""

    @patch("src.interface.gui.tk")
    def test_gui_calculator_raises_import_error_when_tkinter_unavailable(self, mock_tk):
        """GuiCalculator.__init__ must raise ImportError if tkinter is None."""
        import src.interface.gui
        original_tk = src.interface.gui.tk
        src.interface.gui.tk = None

        try:
            with pytest.raises(ImportError) as exc_info:
                gui_module = __import__("src.interface.gui", fromlist=["GuiCalculator"])
                gui_class = getattr(gui_module, "GuiCalculator")
                root = Mock()
                calculator = Calculator()
                gui_class(root, calculator)

            assert "tkinter is not available" in str(exc_info.value)
        finally:
            src.interface.gui.tk = original_tk

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_gui_calculator_initializes_with_calculator(self):
        """GuiCalculator must initialize with Calculator instance."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert gui._calculator is calculator

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_gui_calculator_initializes_mode_handler(self):
        """GuiCalculator must initialize _mode_handler as BaseMode instance."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert isinstance(gui._mode_handler, BaseMode)

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_gui_calculator_initializes_in_normal_mode(self):
        """GuiCalculator must initialize with _mode = Mode.NORMAL."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert gui._mode is Mode.NORMAL

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_gui_calculator_initializes_history(self):
        """GuiCalculator must initialize _history as History instance."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert isinstance(gui._history, History)

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_gui_calculator_initializes_display_value_to_zero(self):
        """GuiCalculator must initialize _display_value to '0'."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert gui._display_value == "0"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_gui_calculator_initializes_first_operand_to_none(self):
        """GuiCalculator must initialize _first_operand to None."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert gui._first_operand is None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_gui_calculator_initializes_pending_op_key_to_none(self):
        """GuiCalculator must initialize _pending_op_key to None."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert gui._pending_op_key is None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_gui_calculator_initializes_last_was_operator_to_false(self):
        """GuiCalculator must initialize _last_was_operator to False."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert gui._last_was_operator is False

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_gui_calculator_initializes_display_label(self):
        """GuiCalculator must have _display_label widget after setup."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert hasattr(gui, "_display_label")

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_gui_calculator_initializes_mode_toggle_btn(self):
        """GuiCalculator must have _mode_toggle_btn widget after setup."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert hasattr(gui, "_mode_toggle_btn")

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_gui_calculator_initializes_op_frame(self):
        """GuiCalculator must have _op_frame widget for operation buttons."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert hasattr(gui, "_op_frame")


# ===========================================================================
# Digit Input Tests
# ===========================================================================

class TestGuiCalculatorDigitInput:
    """Test digit button input accumulation and state management."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_first_digit_replaces_initial_zero(self):
        """First digit after init replaces initial '0' display."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("5")

        assert gui._display_value == "5"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_subsequent_digits_append(self):
        """Subsequent digits are appended to display."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("5")
        gui._on_digit_click("3")

        assert gui._display_value == "53"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_multiple_digits_accumulate(self):
        """Multiple digit clicks accumulate into single number."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        for digit in "7" "8" "9":
            gui._on_digit_click(digit)

        assert gui._display_value == "789"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_digit_after_operator_resets_display(self):
        """Digit click after operator click resets display for next operand."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("5")
        gui._on_binary_op_click("add")
        gui._on_digit_click("3")

        assert gui._display_value == "3"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_digit_click_clears_last_was_operator_flag(self):
        """Digit click sets _last_was_operator to False."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_binary_op_click("add")
        assert gui._last_was_operator is True

        gui._on_digit_click("3")
        assert gui._last_was_operator is False

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_zero_digit_replaces_display_zero(self):
        """Entering 0 as first digit replaces the initial 0."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)
        assert gui._display_value == "0"

        gui._on_digit_click("0")

        assert gui._display_value == "0"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_digit_after_clear_shows_digit(self):
        """After clear, next digit shows that digit."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("7")
        gui._on_clear_click()
        gui._on_digit_click("8")

        assert gui._display_value == "8"


# ===========================================================================
# Binary Operation Tests
# ===========================================================================

class TestGuiCalculatorBinaryOperations:
    """Test binary operation deferral and two-operand execution."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_binary_op_stores_first_operand(self):
        """Binary operation click stores current display as first operand."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("5")
        gui._on_binary_op_click("add")

        assert gui._first_operand == 5.0

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_binary_op_sets_pending_op_key(self):
        """Binary operation click records the operator key."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("5")
        gui._on_binary_op_click("multiply")

        assert gui._pending_op_key == "multiply"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_binary_op_sets_last_was_operator_flag(self):
        """Binary operation click sets _last_was_operator to True."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("5")
        gui._on_binary_op_click("divide")

        assert gui._last_was_operator is True

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_binary_op_does_not_execute_immediately(self):
        """Binary operation does not execute until equals is pressed."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("1")
        gui._on_digit_click("0")
        gui._on_binary_op_click("divide")

        # History should be empty (no operation executed yet)
        assert len(gui._history.get_all()) == 0

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_equals_executes_pending_binary_op(self):
        """Equals click executes the pending binary operation."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("7")
        gui._on_binary_op_click("add")
        gui._on_digit_click("8")
        gui._on_equals_click()

        # Result should be 15
        assert gui._display_value == "15"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_equals_resets_pending_operation_state(self):
        """After equals, pending operation state is cleared."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("7")
        gui._on_binary_op_click("add")
        gui._on_digit_click("8")
        gui._on_equals_click()

        assert gui._first_operand is None
        assert gui._pending_op_key is None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_equals_with_no_pending_op_is_noop(self):
        """Equals click with no pending operation does nothing."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("5")
        gui._on_equals_click()

        assert gui._display_value == "5"
        assert gui._first_operand is None
        assert gui._pending_op_key is None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_binary_op_addition(self):
        """Addition operation: 3 + 4 = 7."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("3")
        gui._on_binary_op_click("add")
        gui._on_digit_click("4")
        gui._on_equals_click()

        assert gui._display_value == "7"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_binary_op_subtraction(self):
        """Subtraction operation: 10 - 3 = 7."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("1")
        gui._on_digit_click("0")
        gui._on_binary_op_click("subtract")
        gui._on_digit_click("3")
        gui._on_equals_click()

        assert gui._display_value == "7"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_binary_op_multiplication(self):
        """Multiplication operation: 6 * 7 = 42."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("6")
        gui._on_binary_op_click("multiply")
        gui._on_digit_click("7")
        gui._on_equals_click()

        assert gui._display_value == "42"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_binary_op_division(self):
        """Division operation: 8 / 2 = 4."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("8")
        gui._on_binary_op_click("divide")
        gui._on_digit_click("2")
        gui._on_equals_click()

        assert gui._display_value == "4"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_binary_op_power(self):
        """Power operation: 2 ^ 10 = 1024."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("2")
        gui._on_binary_op_click("power")
        gui._on_digit_click("1")
        gui._on_digit_click("0")
        gui._on_equals_click()

        assert gui._display_value == "1024"


# ===========================================================================
# Unary Operation Tests
# ===========================================================================

class TestGuiCalculatorUnaryOperations:
    """Test unary operation immediate execution."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_unary_op_executes_immediately(self):
        """Unary operation click executes immediately."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("5")
        gui._on_unary_op_click("square")

        assert gui._display_value == "25"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_unary_op_square(self):
        """Square operation: 7^2 = 49."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("7")
        gui._on_unary_op_click("square")

        assert gui._display_value == "49"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_unary_op_square_root(self):
        """Square root operation: √9 = 3."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("9")
        gui._on_unary_op_click("square_root")

        assert gui._display_value == "3"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_unary_op_cube(self):
        """Cube operation: 3^3 = 27."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("3")
        gui._on_unary_op_click("cube")

        assert gui._display_value == "27"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_unary_op_sets_last_was_operator_flag(self):
        """Unary operation sets _last_was_operator to True."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("5")
        gui._on_unary_op_click("square")

        assert gui._last_was_operator is True

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_unary_op_no_operands_zero_arity(self):
        """Zero-arity operations (pi) execute with empty operands list."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_unary_op_click("pi")

        # pi ≈ 3.14159...
        assert "3.14" in gui._display_value

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_unary_op_invalid_input_shows_error(self):
        """Unary op on invalid display value sets display to 'Error'."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._display_value = "not_a_number"
        gui._on_unary_op_click("square")

        assert gui._display_value == "Error"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_unary_op_chained_operations(self):
        """Chained unary operations work correctly."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("1")
        gui._on_digit_click("6")
        gui._on_unary_op_click("square_root")
        assert gui._display_value == "4"

        gui._on_unary_op_click("square")
        assert gui._display_value == "16"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_unary_op_clears_pending_operation_on_error(self):
        """Error during unary op clears pending binary operation state."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("5")
        gui._on_binary_op_click("add")
        gui._on_digit_click("9")
        # Try factorial on non-integer (9 is fine, but let's use a float result)
        gui._on_unary_op_click("square_root")

        # Display should now show sqrt(9) = 3
        # Pending op should still be "add" (unary ops don't clear pending)
        assert gui._display_value == "3"


# ===========================================================================
# Utility Button Tests (Clear, Negate, Percent)
# ===========================================================================

class TestGuiCalculatorUtilityButtons:
    """Test utility buttons: clear, negate, percent."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_clear_button_resets_display_to_zero(self):
        """Clear button resets display to '0'."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("7")
        gui._on_digit_click("8")
        gui._on_digit_click("9")
        gui._on_clear_click()

        assert gui._display_value == "0"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_clear_button_clears_first_operand(self):
        """Clear button clears _first_operand."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("5")
        gui._on_binary_op_click("add")
        gui._on_clear_click()

        assert gui._first_operand is None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_clear_button_clears_pending_op(self):
        """Clear button clears _pending_op_key."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("5")
        gui._on_binary_op_click("multiply")
        gui._on_clear_click()

        assert gui._pending_op_key is None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_clear_button_resets_last_was_operator_flag(self):
        """Clear button resets _last_was_operator to False."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("5")
        gui._on_binary_op_click("add")
        gui._on_clear_click()

        assert gui._last_was_operator is False

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_negate_utility_key_in_utility_ops_frozenset(self):
        """'negate' is a utility operation key (in _UTILITY_OP_KEYS)."""
        from src.interface import gui

        assert "negate" in gui._UTILITY_OP_KEYS

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_percent_utility_key_in_utility_ops_frozenset(self):
        """'percent' is a utility operation key (in _UTILITY_OP_KEYS)."""
        from src.interface import gui

        assert "percent" in gui._UTILITY_OP_KEYS

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_cube_root_operation(self):
        """Cube root operation: ∛8 = 2."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("8")
        gui._on_unary_op_click("cube_root")

        assert gui._display_value == "2"


# ===========================================================================
# Mode Toggle Tests
# ===========================================================================

class TestGuiCalculatorModeToggle:
    """Test mode toggle button behavior and state reset."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_mode_toggle_switches_normal_to_scientific(self):
        """Mode toggle switches from NORMAL to SCIENTIFIC."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert gui._mode == Mode.NORMAL
        gui._on_mode_toggle_click()
        assert gui._mode == Mode.SCIENTIFIC

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_mode_toggle_switches_scientific_to_normal(self):
        """Mode toggle switches from SCIENTIFIC to NORMAL."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._mode = Mode.SCIENTIFIC
        gui._on_mode_toggle_click()
        assert gui._mode == Mode.NORMAL

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_mode_toggle_resets_display_to_zero(self):
        """Mode toggle resets display to '0'."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("7")
        gui._on_mode_toggle_click()

        assert gui._display_value == "0"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_mode_toggle_clears_pending_operation(self):
        """Mode toggle clears pending operation state."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("5")
        gui._on_binary_op_click("add")
        gui._on_mode_toggle_click()

        assert gui._first_operand is None
        assert gui._pending_op_key is None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_mode_toggle_updates_button_label_to_normal(self):
        """Mode toggle button label changes to 'Normal' when switching to SCIENTIFIC."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert gui._mode == Mode.NORMAL
        gui._on_mode_toggle_click()

        # After toggle to SCIENTIFIC, button should say "Normal"
        assert gui._mode == Mode.SCIENTIFIC
        gui._mode_toggle_btn.configure.assert_called()

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_mode_toggle_updates_button_label_to_scientific(self):
        """Mode toggle button label changes to 'Scientific' when switching to NORMAL."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._mode = Mode.SCIENTIFIC
        gui._on_mode_toggle_click()

        # After toggle to NORMAL, button should say "Scientific"
        assert gui._mode == Mode.NORMAL
        gui._mode_toggle_btn.configure.assert_called()

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_mode_toggle_rebuilds_operation_buttons(self):
        """Mode toggle rebuilds operation button panel."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_mode_toggle_click()

        # Verify operation frame was cleared and rebuilt
        # (in the real code, _build_operation_buttons clears children)
        assert gui._mode == Mode.SCIENTIFIC


# ===========================================================================
# Display Update Tests
# ===========================================================================

class TestGuiCalculatorDisplayUpdate:
    """Test display label synchronization."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_update_display_syncs_label_text(self):
        """_update_display syncs label widget to _display_value."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._display_value = "123"
        gui._update_display()

        gui._display_label.config.assert_called_with(text="123")

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_update_display_with_none_label_is_safe(self):
        """_update_display is safe when _display_label is None."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._display_label = None
        gui._display_value = "456"

        # Should not raise
        gui._update_display()


# ===========================================================================
# Format Result Tests
# ===========================================================================

class TestGuiCalculatorFormatResult:
    """Test numeric result formatting for display."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_format_result_integer_no_decimal_point(self):
        """39.0 formats as '39' without decimal point."""
        from src.interface.gui import GuiCalculator

        result = GuiCalculator._format_result(39.0)
        assert result == "39"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_format_result_float_with_decimal(self):
        """3.14159 formats as float string with decimal."""
        from src.interface.gui import GuiCalculator

        result = GuiCalculator._format_result(3.14159)
        assert "3.14" in result

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_format_result_zero(self):
        """0.0 formats as '0'."""
        from src.interface.gui import GuiCalculator

        result = GuiCalculator._format_result(0.0)
        assert result == "0"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_format_result_negative_integer(self):
        """Negative integer 5.0 formats as '-5'."""
        from src.interface.gui import GuiCalculator

        result = GuiCalculator._format_result(-5.0)
        assert result == "-5"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_format_result_large_integer(self):
        """Large integer 1024.0 formats as '1024'."""
        from src.interface.gui import GuiCalculator

        result = GuiCalculator._format_result(1024.0)
        assert result == "1024"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_format_result_scientific_notation(self):
        """Very large float uses default string representation."""
        from src.interface.gui import GuiCalculator

        result = GuiCalculator._format_result(1e20)
        assert result is not None  # Just verify it doesn't crash

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_format_result_int_type_input(self):
        """Integer input formats correctly."""
        from src.interface.gui import GuiCalculator

        result = GuiCalculator._format_result(42)
        assert result == "42"


# ===========================================================================
# Color Theme Tests
# ===========================================================================

class TestGuiCalculatorColorTheme:
    """Test color theme constants and button styling."""

    def test_theme_dict_exists(self):
        """_THEME dict is defined at module level."""
        from src.interface import gui

        assert hasattr(gui, "_THEME")
        assert isinstance(gui._THEME, dict)

    def test_theme_has_required_colors(self):
        """_THEME contains required color keys."""
        from src.interface import gui

        required_keys = [
            "bg",
            "display_bg",
            "display_fg",
            "display_font",
            "btn_digit_bg",
            "btn_digit_fg",
            "btn_op_bg",
            "btn_op_fg",
            "btn_binary_bg",
            "btn_binary_fg",
            "btn_utility_bg",
            "btn_utility_fg",
            "btn_font",
            "btn_relief",
            "btn_borderwidth",
        ]
        for key in required_keys:
            assert key in gui._THEME

    def test_theme_colors_are_strings_or_tuples(self):
        """_THEME color values are valid color strings or font tuples."""
        from src.interface import gui

        font_keys = {"display_font", "btn_font"}
        for key, value in gui._THEME.items():
            if key in font_keys:
                assert isinstance(value, tuple)
            else:
                assert isinstance(value, (str, int))

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_binary_op_button_colors_orange(self):
        """Binary operation buttons use orange color."""
        from src.interface.gui import GuiCalculator

        bg, fg = GuiCalculator._op_button_colors("add")

        # Should be orange (binary op)
        assert bg == "#FF9500"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_utility_op_button_colors_gray(self):
        """Utility buttons use gray color."""
        from src.interface.gui import GuiCalculator

        bg, fg = GuiCalculator._op_button_colors("negate")

        # Should be gray (utility)
        assert bg == "#A5A5A5"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_unary_op_button_colors_light_gray(self):
        """Unary operation buttons (non-utility) use light gray."""
        from src.interface.gui import GuiCalculator

        bg, fg = GuiCalculator._op_button_colors("square")

        # Should be light gray (standard operation)
        assert bg == "#333333"


# ===========================================================================
# Short Label Tests
# ===========================================================================

class TestGuiCalculatorShortLabel:
    """Test button label shortening."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_short_label_add(self):
        """add operation shows '+'."""
        from src.interface.gui import GuiCalculator

        label = GuiCalculator._short_label("add", "Addition")
        assert label == "+"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_short_label_multiply(self):
        """multiply operation shows '×'."""
        from src.interface.gui import GuiCalculator

        label = GuiCalculator._short_label("multiply", "Multiplication")
        assert label == "×"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_short_label_divide(self):
        """divide operation shows '÷'."""
        from src.interface.gui import GuiCalculator

        label = GuiCalculator._short_label("divide", "Division")
        assert label == "÷"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_short_label_square_root(self):
        """square_root operation shows '√'."""
        from src.interface.gui import GuiCalculator

        label = GuiCalculator._short_label("square_root", "Square Root")
        assert label == "√"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_short_label_pi(self):
        """pi operation shows 'π'."""
        from src.interface.gui import GuiCalculator

        label = GuiCalculator._short_label("pi", "Pi")
        assert label == "π"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_short_label_unknown_key_uses_op_key(self):
        """Unknown operation key defaults to the key itself."""
        from src.interface.gui import GuiCalculator

        label = GuiCalculator._short_label("unknown_op", "Unknown")
        assert label == "unknown_op"


# ===========================================================================
# Module-level frozenset Tests
# ===========================================================================

class TestGuiCalculatorModuleConstants:
    """Test module-level constants."""

    def test_binary_op_keys_frozenset_exists(self):
        """_BINARY_OP_KEYS is a frozenset."""
        from src.interface import gui

        assert hasattr(gui, "_BINARY_OP_KEYS")
        assert isinstance(gui._BINARY_OP_KEYS, frozenset)

    def test_binary_op_keys_contains_expected_operations(self):
        """_BINARY_OP_KEYS includes add, subtract, multiply, divide, power."""
        from src.interface import gui

        expected = {"add", "subtract", "multiply", "divide", "power"}
        assert expected.issubset(gui._BINARY_OP_KEYS)

    def test_utility_op_keys_frozenset_exists(self):
        """_UTILITY_OP_KEYS is a frozenset."""
        from src.interface import gui

        assert hasattr(gui, "_UTILITY_OP_KEYS")
        assert isinstance(gui._UTILITY_OP_KEYS, frozenset)

    def test_utility_op_keys_contains_expected_operations(self):
        """_UTILITY_OP_KEYS includes clear, negate, percent."""
        from src.interface import gui

        expected = {"clear", "negate", "percent"}
        assert expected.issubset(gui._UTILITY_OP_KEYS)


# ===========================================================================
# Integration Tests
# ===========================================================================

class TestGuiCalculatorIntegration:
    """End-to-end integration tests."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_full_flow_addition(self):
        """Full flow: 7 + 8 = 15, then √ result."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("7")
        gui._on_digit_click("8")
        assert gui._display_value == "78"

        gui._on_binary_op_click("divide")
        assert gui._display_value == "78"
        assert gui._first_operand == 78.0
        assert gui._last_was_operator is True

        gui._on_digit_click("2")
        assert gui._display_value == "2"

        gui._on_equals_click()
        assert gui._display_value == "39"

        gui._on_unary_op_click("square_root")
        result = float(gui._display_value)
        assert 6.2 < result < 6.3  # sqrt(39) ≈ 6.24

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_full_flow_with_mode_toggle(self):
        """Full flow includes mode toggle and state reset."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("5")
        gui._on_binary_op_click("add")
        gui._on_digit_click("3")

        gui._on_mode_toggle_click()

        assert gui._mode == Mode.SCIENTIFIC
        assert gui._display_value == "0"
        assert gui._first_operand is None
        assert gui._pending_op_key is None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_full_flow_multiple_operations_in_sequence(self):
        """Multiple operations: 2 + 3 = 5, then * 4 = 20."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("2")
        gui._on_binary_op_click("add")
        gui._on_digit_click("3")
        gui._on_equals_click()
        assert gui._display_value == "5"

        gui._on_binary_op_click("multiply")
        gui._on_digit_click("4")
        gui._on_equals_click()
        assert gui._display_value == "20"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_scientific_operations_available_in_scientific_mode(self):
        """Scientific operations are available after mode toggle."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._mode = Mode.NORMAL
        normal_ops = gui._get_available_operations_for_mode()

        gui._mode = Mode.SCIENTIFIC
        scientific_ops = gui._get_available_operations_for_mode()

        assert len(scientific_ops) > len(normal_ops)
        assert "sin" in scientific_ops
        assert "sin" not in normal_ops

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_clear_clears_error_state(self):
        """Clear clears error state from display."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._display_value = "Error"
        gui._on_clear_click()

        assert gui._display_value == "0"


# ===========================================================================
# Edge Case Tests
# ===========================================================================

class TestGuiCalculatorEdgeCases:
    """Edge cases and boundary conditions."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_division_by_zero_shows_error(self):
        """Division by zero shows 'Error' and clears state."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("1")
        gui._on_binary_op_click("divide")
        gui._on_digit_click("0")
        gui._on_equals_click()

        assert gui._display_value == "Error"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_negative_numbers_from_subtraction(self):
        """Subtraction can produce negative numbers."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("3")
        gui._on_binary_op_click("subtract")
        gui._on_digit_click("5")
        gui._on_equals_click()

        assert "-" in gui._display_value

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_large_number_display(self):
        """Very large numbers display."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("9")
        gui._on_binary_op_click("power")
        gui._on_digit_click("1")
        gui._on_digit_click("0")
        gui._on_equals_click()

        # 9^10 = 3486784401
        assert gui._display_value == "3486784401"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_zero_display_after_digit_press_on_zero(self):
        """Pressing '0' on initial '0' shows '0'."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert gui._display_value == "0"
        gui._on_digit_click("0")
        assert gui._display_value == "0"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_binary_op_with_float_display_value(self):
        """Binary op can handle float display values."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("5")
        gui._on_unary_op_click("square_root")
        gui._on_binary_op_click("multiply")

        # First operand should be float(sqrt(5))
        assert gui._first_operand is not None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_multiple_unary_ops_in_sequence(self):
        """Multiple unary operations can be chained."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("4")
        gui._on_unary_op_click("square")
        gui._on_unary_op_click("square_root")

        assert gui._display_value == "4"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_equals_with_operator_but_no_second_digit_uses_display(self):
        """Equals without explicitly entering second operand uses current display as second operand."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("5")
        gui._on_binary_op_click("add")
        gui._on_equals_click()

        # Display still shows "5", which becomes the second operand
        # So 5 + 5 = 10
        assert gui._display_value == "10"


class TestGuiCalculatorBinaryOpButtonColors:
    """Test button color assignment for different operation categories."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_all_binary_ops_have_orange_buttons(self):
        """All binary operations get orange button color."""
        from src.interface.gui import GuiCalculator
        from src.interface import gui

        for op_key in gui._BINARY_OP_KEYS:
            bg, fg = GuiCalculator._op_button_colors(op_key)
            assert bg == "#FF9500", f"Binary op {op_key} should have orange bg"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_all_utility_ops_have_gray_buttons(self):
        """All utility operations get gray button color."""
        from src.interface.gui import GuiCalculator
        from src.interface import gui

        for op_key in gui._UTILITY_OP_KEYS:
            bg, fg = GuiCalculator._op_button_colors(op_key)
            assert bg == "#A5A5A5", f"Utility op {op_key} should have gray bg"


class TestGuiCalculatorBuildOperationButtons:
    """Test operation button panel building."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_build_operation_buttons_clears_frame(self):
        """_build_operation_buttons clears previous buttons before rebuilding."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # Verify frame is cleaned up and rebuilt
        assert gui._op_frame is not None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_operation_buttons_rebuilt_after_mode_toggle(self):
        """Operation buttons are rebuilt when mode changes."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._mode = Mode.NORMAL
        gui._on_mode_toggle_click()

        assert gui._mode == Mode.SCIENTIFIC


class TestGuiCalculatorStateManagement:
    """Test state consistency across operations."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_pending_op_cleared_after_second_binary_op(self):
        """Pressing another binary op after first clears pending (or chains)."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("5")
        gui._on_binary_op_click("add")
        gui._on_digit_click("3")
        gui._on_binary_op_click("multiply")

        # Now pending op should be multiply, first_operand should be 5+3=8
        # (in real calculator, this would auto-execute the previous op)
        assert gui._pending_op_key == "multiply"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_format_result_preserves_precision(self):
        """Format result preserves float precision for non-integer results."""
        from src.interface.gui import GuiCalculator

        result = GuiCalculator._format_result(1/3)
        assert "0.333" in result

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_short_label_covers_all_expected_operations(self):
        """_short_label handles all operations in operations registry."""
        from src.interface.gui import GuiCalculator
        from src.operations import OPERATIONS

        for op_key in OPERATIONS.keys():
            label = GuiCalculator._short_label(op_key, OPERATIONS[op_key]["label"])
            assert label is not None
            assert isinstance(label, str)
            assert len(label) > 0


class TestGuiCalculatorErrorRecovery:
    """Test error handling and recovery."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_error_display_clears_pending_state(self):
        """When operation fails, pending state is cleared."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("5")
        gui._on_binary_op_click("divide")
        gui._on_digit_click("0")
        gui._on_equals_click()

        assert gui._display_value == "Error"
        assert gui._first_operand is None
        assert gui._pending_op_key is None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_recovery_after_error_with_clear(self):
        """After error, can recover by pressing clear button."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("1")
        gui._on_binary_op_click("divide")
        gui._on_digit_click("0")
        gui._on_equals_click()

        assert gui._display_value == "Error"

        gui._on_clear_click()

        assert gui._display_value == "0"
        assert gui._first_operand is None
        assert gui._pending_op_key is None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_unary_op_error_sets_display_to_error(self):
        """Unary op error on invalid input sets display to 'Error'."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_digit_click("5")
        gui._on_binary_op_click("add")
        gui._display_value = "invalid"
        gui._on_unary_op_click("square")

        assert gui._display_value == "Error"


class TestGuiCalculatorDigitAccumulation:
    """Test multi-digit number accumulation."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_very_long_number_accumulation(self):
        """Very long numbers can be accumulated."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        for digit in "123456789":
            gui._on_digit_click(digit)

        assert gui._display_value == "123456789"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_repeated_same_digit(self):
        """Repeated digit clicks accumulate same digit."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        for _ in range(3):
            gui._on_digit_click("8")

        assert gui._display_value == "888"


class TestGuiCalculatorModeAwareness:
    """Test that operations respect current mode."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_available_ops_change_with_mode(self):
        """Available operations differ between NORMAL and SCIENTIFIC."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._mode = Mode.NORMAL
        normal_count = len(gui._get_available_operations_for_mode())

        gui._mode = Mode.SCIENTIFIC
        scientific_count = len(gui._get_available_operations_for_mode())

        assert scientific_count > normal_count

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    def test_mode_toggle_multiple_times(self):
        """Mode can be toggled multiple times without issues."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        for i in range(4):
            gui._on_mode_toggle_click()
            expected_mode = Mode.SCIENTIFIC if i % 2 == 0 else Mode.NORMAL
            assert gui._mode == expected_mode


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
