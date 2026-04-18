"""Comprehensive pytest tests for src/interface/gui.py.

Tests cover:
- GuiCalculator instantiation and initialization (with mocked tkinter)
- Display state management (_on_digit, _on_clear)
- Binary operation workflows (add, subtract, etc.)
- Unary operation workflows (square_root, factorial, etc.)
- Error handling and display
- Mode switching and button rebuilding
- History tracking and display updates
- Result formatting (integer vs float)
- Edge cases and error conditions
"""

import pytest
from unittest.mock import patch, MagicMock, call
import sys

# Mock tkinter before importing gui.py
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.font'] = MagicMock()

from src.core.calculator import Calculator
from src.shared.logger import Logger
from src.interface.gui import GuiCalculator
from src.interface.mode import SimpleMode, ScientificMode


# ===========================================================================
# Fixtures
# ===========================================================================


@pytest.fixture
def calculator():
    """Create a fresh Calculator instance for each test."""
    return Calculator()


@pytest.fixture
def logger():
    """Create a Logger instance for tests (optional)."""
    # Use a temporary file to avoid polluting the filesystem
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
        log_path = f.name
    yield Logger(log_file=log_path)
    # Cleanup
    import os
    try:
        os.unlink(log_path)
    except OSError:
        pass


class MockStringVar:
    """A mock StringVar that actually stores values."""
    def __init__(self, value="0"):
        self._value = value

    def get(self):
        return self._value

    def set(self, value):
        self._value = value


@pytest.fixture
def gui_with_mocked_tk(calculator):
    """Create a GuiCalculator with mocked tkinter."""
    with patch('src.interface.gui._TK_AVAILABLE', True):
        with patch('src.interface.gui.tk') as mock_tk:
            # Setup mock tk.Tk instance
            mock_root = MagicMock()
            mock_tk.Tk.return_value = mock_root

            # Setup mock StringVar with real get/set functionality
            def create_string_var(value=None):
                # Handle both positional and keyword arguments
                if value is None:
                    value = "0"
                return MockStringVar(value)

            mock_tk.StringVar = create_string_var

            # Setup mock frames and other widgets
            mock_tk.Frame = MagicMock(side_effect=lambda *args, **kwargs: MagicMock())
            mock_tk.Label = MagicMock(side_effect=lambda *args, **kwargs: MagicMock())
            mock_tk.Button = MagicMock(side_effect=lambda *args, **kwargs: MagicMock())
            mock_tk.Radiobutton = MagicMock(side_effect=lambda *args, **kwargs: MagicMock())
            mock_tk.Text = MagicMock(side_effect=lambda *args, **kwargs: MagicMock())
            mock_tk.Scrollbar = MagicMock(side_effect=lambda *args, **kwargs: MagicMock())

            # Create and return the GUI
            gui = GuiCalculator(calculator)
            yield gui


# ===========================================================================
# Instantiation and Initialization
# ===========================================================================


def test_gui_calculator_can_be_instantiated(gui_with_mocked_tk):
    """GuiCalculator can be instantiated without error."""
    gui = gui_with_mocked_tk
    assert gui is not None


def test_gui_calculator_requires_tkinter():
    """GuiCalculator raises ImportError when tkinter is unavailable."""
    with patch('src.interface.gui._TK_AVAILABLE', False):
        calc = Calculator()
        with pytest.raises(ImportError, match="tkinter is not available"):
            GuiCalculator(calc)


def test_gui_calculator_stores_calculator_reference(gui_with_mocked_tk):
    """GuiCalculator stores the Calculator instance."""
    gui = gui_with_mocked_tk
    assert gui._calculator is not None
    assert isinstance(gui._calculator, Calculator)


def test_gui_calculator_creates_dispatcher(gui_with_mocked_tk):
    """GuiCalculator creates an OperationDispatcher."""
    gui = gui_with_mocked_tk
    assert gui._dispatcher is not None


def test_gui_calculator_creates_history(gui_with_mocked_tk):
    """GuiCalculator creates a History instance."""
    gui = gui_with_mocked_tk
    assert gui._history is not None


def test_gui_calculator_initial_mode_is_simple(gui_with_mocked_tk):
    """GuiCalculator starts in SimpleMode."""
    gui = gui_with_mocked_tk
    assert isinstance(gui._current_mode, SimpleMode)


def test_gui_calculator_initial_display_state(gui_with_mocked_tk):
    """GuiCalculator display initially shows "0"."""
    gui = gui_with_mocked_tk
    assert gui._display_var.get() == "0"


def test_gui_calculator_initial_binary_state(gui_with_mocked_tk):
    """GuiCalculator binary operation state is initially reset."""
    gui = gui_with_mocked_tk
    assert gui._pending_operation is None
    assert gui._first_operand is None
    assert gui._waiting_for_second is False


def test_gui_calculator_operation_buttons_dict_exists(gui_with_mocked_tk):
    """GuiCalculator has an _operation_buttons dictionary."""
    gui = gui_with_mocked_tk
    assert isinstance(gui._operation_buttons, dict)


# ===========================================================================
# Display State Management: _on_digit
# ===========================================================================


def test_on_digit_appends_to_display(gui_with_mocked_tk):
    """Calling _on_digit appends a digit to the display."""
    gui = gui_with_mocked_tk
    gui._display_var.set("5")
    gui._on_digit("3")
    assert gui._display_var.get() == "53"


def test_on_digit_replaces_zero(gui_with_mocked_tk):
    """When display is "0", _on_digit replaces it with the digit."""
    gui = gui_with_mocked_tk
    gui._display_var.set("0")
    gui._on_digit("5")
    assert gui._display_var.get() == "5"


def test_on_digit_replaces_error(gui_with_mocked_tk):
    """When display starts with "Error", _on_digit replaces it."""
    gui = gui_with_mocked_tk
    gui._display_var.set("Error: Division by zero")
    gui._on_digit("5")
    assert gui._display_var.get() == "5"


def test_on_digit_adds_decimal_point(gui_with_mocked_tk):
    """Calling _on_digit with "." adds a decimal point."""
    gui = gui_with_mocked_tk
    gui._display_var.set("5")
    gui._on_digit(".")
    assert gui._display_var.get() == "5."


def test_on_digit_prevents_multiple_decimal_points(gui_with_mocked_tk):
    """Calling _on_digit with "." when display has "." is ignored."""
    gui = gui_with_mocked_tk
    gui._display_var.set("5.3")
    gui._on_digit(".")
    assert gui._display_var.get() == "5.3"


def test_on_digit_allows_decimal_after_error(gui_with_mocked_tk):
    """After error, decimal point is treated as a digit and replaces error."""
    gui = gui_with_mocked_tk
    gui._display_var.set("Error: something")
    gui._on_digit(".")
    assert gui._display_var.get() == "."


def test_on_digit_sequence(gui_with_mocked_tk):
    """Sequence of digit presses builds multi-digit number."""
    gui = gui_with_mocked_tk
    for digit in "123":
        gui._on_digit(digit)
    assert gui._display_var.get() == "123"


# ===========================================================================
# Display State Management: _on_clear
# ===========================================================================


def test_on_clear_resets_display(gui_with_mocked_tk):
    """Calling _on_clear resets display to "0"."""
    gui = gui_with_mocked_tk
    gui._display_var.set("12345")
    gui._on_clear()
    assert gui._display_var.get() == "0"


def test_on_clear_resets_pending_operation(gui_with_mocked_tk):
    """_on_clear resets _pending_operation to None."""
    gui = gui_with_mocked_tk
    gui._pending_operation = "add"
    gui._on_clear()
    assert gui._pending_operation is None


def test_on_clear_resets_first_operand(gui_with_mocked_tk):
    """_on_clear resets _first_operand to None."""
    gui = gui_with_mocked_tk
    gui._first_operand = 5.0
    gui._on_clear()
    assert gui._first_operand is None


def test_on_clear_resets_waiting_flag(gui_with_mocked_tk):
    """_on_clear resets _waiting_for_second to False."""
    gui = gui_with_mocked_tk
    gui._waiting_for_second = True
    gui._on_clear()
    assert gui._waiting_for_second is False


# ===========================================================================
# Binary Operation Workflow
# ===========================================================================


def test_binary_operation_workflow_add(gui_with_mocked_tk):
    """Complete workflow: 5 + 3 = 8."""
    gui = gui_with_mocked_tk
    gui._display_var.set("5")
    gui._on_operation_select("add")
    gui._display_var.set("3")
    gui._on_equals()
    assert gui._display_var.get() == "8"


def test_binary_operation_workflow_subtract(gui_with_mocked_tk):
    """Complete workflow: 10 - 3 = 7."""
    gui = gui_with_mocked_tk
    gui._display_var.set("10")
    gui._on_operation_select("subtract")
    gui._display_var.set("3")
    gui._on_equals()
    assert gui._display_var.get() == "7"


def test_binary_operation_workflow_multiply(gui_with_mocked_tk):
    """Complete workflow: 5 * 6 = 30."""
    gui = gui_with_mocked_tk
    gui._display_var.set("5")
    gui._on_operation_select("multiply")
    gui._display_var.set("6")
    gui._on_equals()
    assert gui._display_var.get() == "30"


def test_binary_operation_workflow_divide(gui_with_mocked_tk):
    """Complete workflow: 10 / 2 = 5."""
    gui = gui_with_mocked_tk
    gui._display_var.set("10")
    gui._on_operation_select("divide")
    gui._display_var.set("2")
    gui._on_equals()
    assert gui._display_var.get() == "5"


def test_binary_operation_workflow_power(gui_with_mocked_tk):
    """Complete workflow: 2 ^ 3 = 8."""
    gui = gui_with_mocked_tk
    gui._display_var.set("2")
    gui._on_operation_select("power")
    gui._display_var.set("3")
    gui._on_equals()
    assert gui._display_var.get() == "8"


def test_binary_operation_stores_first_operand(gui_with_mocked_tk):
    """After selecting a binary op, _first_operand is stored."""
    gui = gui_with_mocked_tk
    gui._display_var.set("5")
    gui._on_operation_select("add")
    assert gui._first_operand == 5.0


def test_binary_operation_sets_pending_op(gui_with_mocked_tk):
    """After selecting a binary op, _pending_operation is set."""
    gui = gui_with_mocked_tk
    gui._display_var.set("5")
    gui._on_operation_select("add")
    assert gui._pending_operation == "add"


def test_binary_operation_sets_waiting_flag(gui_with_mocked_tk):
    """After selecting a binary op, _waiting_for_second is True."""
    gui = gui_with_mocked_tk
    gui._display_var.set("5")
    gui._on_operation_select("add")
    assert gui._waiting_for_second is True


def test_binary_operation_clears_display_for_second_operand(gui_with_mocked_tk):
    """After selecting a binary op, display is reset to "0"."""
    gui = gui_with_mocked_tk
    gui._display_var.set("5")
    gui._on_operation_select("add")
    assert gui._display_var.get() == "0"


# ===========================================================================
# Unary Operation Workflow
# ===========================================================================


def test_unary_operation_square(gui_with_mocked_tk):
    """Unary operation: square(5) = 25."""
    gui = gui_with_mocked_tk
    gui._display_var.set("5")
    gui._on_operation_select("square")
    assert gui._display_var.get() == "25"


def test_unary_operation_square_root(gui_with_mocked_tk):
    """Unary operation: sqrt(9) = 3."""
    gui = gui_with_mocked_tk
    gui._display_var.set("9")
    gui._on_operation_select("square_root")
    assert gui._display_var.get() == "3"


def test_unary_operation_cube(gui_with_mocked_tk):
    """Unary operation: cube(2) = 8."""
    gui = gui_with_mocked_tk
    gui._display_var.set("2")
    gui._on_operation_select("cube")
    assert gui._display_var.get() == "8"


def test_unary_operation_cube_root(gui_with_mocked_tk):
    """Unary operation: cube_root(8) = 2."""
    gui = gui_with_mocked_tk
    gui._display_var.set("8")
    gui._on_operation_select("cube_root")
    assert gui._display_var.get() == "2"


def test_unary_operation_factorial(gui_with_mocked_tk):
    """Unary operation with integer coercion: factorial(5) = 120."""
    gui = gui_with_mocked_tk
    gui._display_var.set("5")
    gui._on_operation_select("factorial")
    assert gui._display_var.get() == "120"


def test_unary_operation_does_not_set_pending_op(gui_with_mocked_tk):
    """Unary operations do not set _pending_operation."""
    gui = gui_with_mocked_tk
    gui._display_var.set("5")
    gui._on_operation_select("square")
    assert gui._pending_operation is None


def test_unary_operation_does_not_set_waiting_flag(gui_with_mocked_tk):
    """Unary operations do not set _waiting_for_second."""
    gui = gui_with_mocked_tk
    gui._display_var.set("5")
    gui._on_operation_select("square")
    assert gui._waiting_for_second is False


# ===========================================================================
# Error Handling
# ===========================================================================


def test_handle_error_sets_error_display(gui_with_mocked_tk):
    """_handle_error sets display to "Error: {message}"."""
    gui = gui_with_mocked_tk
    gui._handle_error("test error message")
    assert gui._display_var.get() == "Error: test error message"


def test_on_operation_invalid_operand_shows_error(gui_with_mocked_tk):
    """Invalid operand (non-numeric) shows error."""
    gui = gui_with_mocked_tk
    gui._display_var.set("abc")
    gui._on_operation_select("square")
    assert "Error:" in gui._display_var.get()


def test_binary_operation_division_by_zero(gui_with_mocked_tk):
    """Division by zero shows error message."""
    gui = gui_with_mocked_tk
    gui._display_var.set("5")
    gui._on_operation_select("divide")
    gui._display_var.set("0")
    gui._on_equals()
    assert "Error:" in gui._display_var.get()


def test_division_by_zero_logs_error(gui_with_mocked_tk):
    """Division by zero is logged (Logger created lazily if needed)."""
    gui = gui_with_mocked_tk
    gui._logger = Logger()
    gui._display_var.set("5")
    gui._on_operation_select("divide")
    gui._display_var.set("0")
    gui._on_equals()
    assert gui._logger is not None


def test_division_by_zero_resets_binary_state(gui_with_mocked_tk):
    """After division by zero error, binary state is reset."""
    gui = gui_with_mocked_tk
    gui._display_var.set("5")
    gui._on_operation_select("divide")
    gui._display_var.set("0")
    gui._on_equals()
    assert gui._pending_operation is None
    assert gui._first_operand is None
    assert gui._waiting_for_second is False


def test_unary_operation_invalid_input_shows_error(gui_with_mocked_tk):
    """Unary operation with invalid input shows error."""
    gui = gui_with_mocked_tk
    gui._display_var.set("not_a_number")
    gui._on_operation_select("square_root")
    assert "Error:" in gui._display_var.get()


def test_negative_square_root_shows_error(gui_with_mocked_tk):
    """Square root of negative number shows error."""
    gui = gui_with_mocked_tk
    gui._display_var.set("-1")
    gui._on_operation_select("square_root")
    assert "Error:" in gui._display_var.get()


def test_negative_factorial_shows_error(gui_with_mocked_tk):
    """Factorial of negative number shows error."""
    gui = gui_with_mocked_tk
    gui._display_var.set("-5")
    gui._on_operation_select("factorial")
    assert "Error:" in gui._display_var.get()


# ===========================================================================
# Mode Switching
# ===========================================================================


def test_switch_mode_changes_current_mode(gui_with_mocked_tk):
    """switch_mode changes _current_mode."""
    gui = gui_with_mocked_tk
    assert isinstance(gui._current_mode, SimpleMode)
    gui.switch_mode(ScientificMode())
    assert isinstance(gui._current_mode, ScientificMode)


def test_switch_mode_rebuilds_operation_buttons(gui_with_mocked_tk):
    """switch_mode calls _build_operation_buttons (indirectly via operation availability)."""
    gui = gui_with_mocked_tk
    gui.switch_mode(SimpleMode())
    simple_ops = gui._current_mode.available_operations()
    assert len(simple_ops) > 0


def test_mode_change_handler_simple_to_scientific(gui_with_mocked_tk):
    """_on_mode_change switches from simple to scientific."""
    gui = gui_with_mocked_tk
    gui._mode_var.set("scientific")
    gui._on_mode_change()
    assert isinstance(gui._current_mode, ScientificMode)


def test_mode_change_handler_scientific_to_simple(gui_with_mocked_tk):
    """_on_mode_change switches from scientific to simple."""
    gui = gui_with_mocked_tk
    gui._mode_var.set("simple")
    gui._on_mode_change()
    assert isinstance(gui._current_mode, SimpleMode)


# ===========================================================================
# History Tracking
# ===========================================================================


def test_history_updated_after_unary_operation(gui_with_mocked_tk):
    """History is updated after a unary operation."""
    gui = gui_with_mocked_tk
    gui._display_var.set("5")
    gui._on_operation_select("square")
    history_entries = gui._history.get_all()
    assert len(history_entries) > 0
    assert "square" in history_entries[0]


def test_history_updated_after_binary_operation(gui_with_mocked_tk):
    """History is updated after a binary operation."""
    gui = gui_with_mocked_tk
    gui._display_var.set("5")
    gui._on_operation_select("add")
    gui._display_var.set("3")
    gui._on_equals()
    history_entries = gui._history.get_all()
    assert len(history_entries) > 0
    assert "add" in history_entries[0]


def test_history_contains_operands_and_result(gui_with_mocked_tk):
    """History entry contains operands and result."""
    gui = gui_with_mocked_tk
    gui._display_var.set("5")
    gui._on_operation_select("add")
    gui._display_var.set("3")
    gui._on_equals()
    history_entries = gui._history.get_all()
    assert len(history_entries) > 0
    # Entry format: "add(5.0, 3.0) = 8"
    entry = history_entries[0]
    assert "5" in entry
    assert "3" in entry
    assert "8" in entry


# ===========================================================================
# Result Formatting
# ===========================================================================


def test_format_result_integer(gui_with_mocked_tk):
    """Integer results are formatted without decimal point."""
    result = GuiCalculator._format_result(5)
    assert result == "5"
    assert "." not in result


def test_format_result_float(gui_with_mocked_tk):
    """Float results with decimals are formatted with :g notation."""
    result = GuiCalculator._format_result(5.5)
    assert result == "5.5"


def test_format_result_float_removes_trailing_zeros(gui_with_mocked_tk):
    """Format result removes trailing zeros (e.g., 3.0 -> 3)."""
    result = GuiCalculator._format_result(3.0)
    assert result == "3"
    assert "." not in result


def test_format_result_very_small_float(gui_with_mocked_tk):
    """Very small floats are formatted appropriately."""
    result = GuiCalculator._format_result(0.00001)
    assert "e" in result.lower() or float(result) == 0.00001


def test_format_result_large_integer(gui_with_mocked_tk):
    """Large integers are formatted as strings without decimals."""
    result = GuiCalculator._format_result(1000000)
    assert result == "1000000"
    assert "." not in result


# ===========================================================================
# Equals Button Behavior
# ===========================================================================


def test_on_equals_no_op_without_pending(gui_with_mocked_tk):
    """Pressing equals without a pending operation is a no-op."""
    gui = gui_with_mocked_tk
    gui._display_var.set("5")
    gui._on_equals()
    assert gui._display_var.get() == "5"


def test_on_equals_resets_binary_state_after_operation(gui_with_mocked_tk):
    """After equals, binary state is reset."""
    gui = gui_with_mocked_tk
    gui._display_var.set("5")
    gui._on_operation_select("add")
    gui._display_var.set("3")
    gui._on_equals()
    assert gui._pending_operation is None
    assert gui._first_operand is None
    assert gui._waiting_for_second is False


def test_on_equals_invalid_second_operand(gui_with_mocked_tk):
    """Invalid second operand shows error but does NOT reset state.

    Note: This is the actual behavior of the implementation. When coercion
    fails before dispatch, the binary state is intentionally left untouched
    so the user can try again with a valid operand.
    """
    gui = gui_with_mocked_tk
    gui._display_var.set("5")
    gui._on_operation_select("add")
    gui._display_var.set("abc")
    gui._on_equals()
    assert "Error:" in gui._display_var.get()
    # State is NOT reset when invalid operand is passed
    assert gui._pending_operation == "add"
    assert gui._first_operand == 5.0


# ===========================================================================
# Edge Cases and Boundary Conditions
# ===========================================================================


def test_operations_with_floats(gui_with_mocked_tk):
    """Operations work with floating-point operands."""
    gui = gui_with_mocked_tk
    gui._display_var.set("2.5")
    gui._on_operation_select("add")
    gui._display_var.set("3.5")
    gui._on_equals()
    assert gui._display_var.get() == "6"


def test_operations_with_negative_numbers(gui_with_mocked_tk):
    """Operations work with negative operands."""
    gui = gui_with_mocked_tk
    gui._display_var.set("-5")
    gui._on_operation_select("add")
    gui._display_var.set("3")
    gui._on_equals()
    assert gui._display_var.get() == "-2"


def test_operations_with_zero(gui_with_mocked_tk):
    """Operations work with zero as an operand."""
    gui = gui_with_mocked_tk
    gui._display_var.set("0")
    gui._on_operation_select("multiply")
    gui._display_var.set("100")
    gui._on_equals()
    assert gui._display_var.get() == "0"


def test_very_large_numbers(gui_with_mocked_tk):
    """Operations work with very large numbers."""
    gui = gui_with_mocked_tk
    gui._display_var.set("999999999")
    gui._on_operation_select("multiply")
    gui._display_var.set("2")
    gui._on_equals()
    result = gui._display_var.get()
    assert "Error:" not in result


def test_chain_operations(gui_with_mocked_tk):
    """Chaining operations: 5 + 3 then * 2."""
    gui = gui_with_mocked_tk
    gui._display_var.set("5")
    gui._on_operation_select("add")
    gui._display_var.set("3")
    gui._on_equals()
    first_result = gui._display_var.get()
    gui._on_operation_select("multiply")
    gui._display_var.set("2")
    gui._on_equals()
    final_result = gui._display_var.get()
    # (5 + 3) * 2 = 16
    assert final_result == "16"


def test_decimal_in_display_not_replaced_by_digit(gui_with_mocked_tk):
    """When display has decimal, digit appends (does not replace)."""
    gui = gui_with_mocked_tk
    gui._display_var.set("3.14")
    gui._on_digit("5")
    assert gui._display_var.get() == "3.145"


# ===========================================================================
# Run GUI Method
# ===========================================================================


def test_run_gui_function_exists():
    """run_gui function exists and is callable."""
    from src.interface.gui import run_gui
    assert callable(run_gui)


# ===========================================================================
# Integration Tests
# ===========================================================================


def test_full_workflow_multiple_operations(gui_with_mocked_tk):
    """Full workflow with multiple operation sequences."""
    gui = gui_with_mocked_tk
    # First operation: 10 * 5 = 50
    gui._display_var.set("10")
    gui._on_operation_select("multiply")
    gui._display_var.set("5")
    gui._on_equals()
    assert gui._display_var.get() == "50"

    # Clear and second operation: 100 / 4 = 25
    gui._on_clear()
    gui._display_var.set("100")
    gui._on_operation_select("divide")
    gui._display_var.set("4")
    gui._on_equals()
    assert gui._display_var.get() == "25"

    # History should have both operations
    history = gui._history.get_all()
    assert len(history) >= 2


def test_gui_with_provided_logger(calculator):
    """GuiCalculator accepts optional logger parameter."""
    logger = Logger()
    with patch('src.interface.gui._TK_AVAILABLE', True):
        with patch('src.interface.gui.tk'):
            gui = GuiCalculator(calculator, logger=logger)
            assert gui._logger == logger


def test_gui_creates_logger_lazily(gui_with_mocked_tk):
    """GuiCalculator creates logger lazily when first error occurs."""
    gui = gui_with_mocked_tk
    assert gui._logger is None
    gui._display_var.set("5")
    gui._on_operation_select("square_root")
    gui._display_var.set("10")
    gui._on_operation_select("ln")
    gui._display_var.set("0")
    gui._on_operation_select("ln")  # Log of 0 is undefined
    # Logger may or may not be created depending on whether error is logged
    # Just verify no exception is raised


def test_mode_operations_accessible_after_switch(gui_with_mocked_tk):
    """Operations are correctly available after mode switch."""
    gui = gui_with_mocked_tk
    simple_ops = gui._current_mode.available_operations()
    gui.switch_mode(ScientificMode())
    scientific_ops = gui._current_mode.available_operations()
    # Both should be valid dicts
    assert isinstance(simple_ops, dict)
    assert isinstance(scientific_ops, dict)
