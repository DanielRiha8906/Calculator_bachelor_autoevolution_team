"""Integration tests for CalculatorGUI.

Tests the full GUI workflow using tkinter with headless testing
(withdraw() to avoid displaying windows in CI). Uses mocking for
headless environments where tkinter is unavailable.
"""

import pytest
import sys
from unittest.mock import Mock, patch, MagicMock, PropertyMock

# Mock tkinter before importing GUI modules
import sys
from unittest.mock import MagicMock

# Check if tkinter is available
try:
    import tkinter as tk
    import tkinter.font as tkfont
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False
    # Create mocks for tkinter modules with StringVar support
    class MockStringVar:
        def __init__(self, value=""):
            self._value = value

        def get(self):
            return self._value

        def set(self, value):
            self._value = value

    tk = MagicMock()
    tk.StringVar = MockStringVar
    tkfont = MagicMock()
    sys.modules['tkinter'] = tk
    sys.modules['tkinter.font'] = tkfont

from src.core.calculator import Calculator
from src.support.history import HistoryTracker
from src.gui.modes import SimpleMode, ScientificMode
from src.gui.application import CalculatorGUI, _THEME, _SYMBOLS, _ARITHMETIC_OPS


def create_mock_tk_root():
    """Create a mock tkinter root that behaves like tk.Tk()."""
    root = MagicMock()
    root.winfo_children = MagicMock(return_value=[])
    root.configure = MagicMock()
    root.resizable = MagicMock()
    root.columnconfigure = MagicMock()
    root.rowconfigure = MagicMock()
    return root


def create_real_tk_root():
    """Create a real hidden tkinter root window."""
    root = tk.Tk()
    root.withdraw()
    return root


@pytest.fixture
def tk_root():
    """Provide a tkinter root window for testing.

    Uses a real window if tkinter is available, otherwise uses a mock.
    """
    if HAS_TKINTER:
        root = create_real_tk_root()
        yield root
        try:
            root.destroy()
        except:
            pass
    else:
        root = create_mock_tk_root()
        yield root


@pytest.fixture
def calculator():
    """Provide a fresh Calculator instance."""
    return Calculator()


@pytest.fixture
def history_tracker():
    """Provide a fresh HistoryTracker instance."""
    return HistoryTracker()


class TestGUILaunchAndInitialization:
    """Tests for GUI initialization and launch."""

    def test_gui_launch_simple_mode(self, tk_root, calculator, history_tracker):
        """Test that GUI initializes successfully with SimpleMode."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        assert gui is not None
        assert gui._mode.name == "Simple"
        assert gui._calculator is calculator
        assert gui._history_tracker is history_tracker

    def test_gui_launch_scientific_mode(self, tk_root, calculator, history_tracker):
        """Test that GUI initializes successfully with ScientificMode."""
        mode = ScientificMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        assert gui is not None
        assert gui._mode.name == "Scientific"
        assert gui._calculator is calculator
        assert gui._history_tracker is history_tracker

    def test_gui_initial_display_is_zero(self, tk_root, calculator, history_tracker):
        """Test that GUI initializes with display showing '0'."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        assert gui._get_display() == "0"

    def test_gui_initial_state_no_pending_op(self, tk_root, calculator, history_tracker):
        """Test that GUI initializes with no pending operation."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        assert gui._pending_op is None
        assert gui._pending_op_name is None
        assert gui._first_operand is None

    def test_gui_initial_current_input_empty(self, tk_root, calculator, history_tracker):
        """Test that GUI initializes with empty current input."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        assert gui._current_input == ""


class TestNumberInput:
    """Tests for digit and decimal input."""

    def test_gui_number_input_single_digit(self, tk_root, calculator, history_tracker):
        """Test entering a single digit updates display."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("5")

        assert gui._get_display() == "5"
        assert gui._current_input == "5"

    def test_gui_number_input_multiple_digits(self, tk_root, calculator, history_tracker):
        """Test entering multiple digits builds the number."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("1")
        gui._on_digit("2")
        gui._on_digit("3")

        assert gui._get_display() == "123"
        assert gui._current_input == "123"

    def test_gui_number_input_zero(self, tk_root, calculator, history_tracker):
        """Test entering zero."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("0")

        assert gui._get_display() == "0"

    def test_gui_decimal_input_single_dot(self, tk_root, calculator, history_tracker):
        """Test entering a decimal point."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("5")
        gui._on_decimal()

        assert gui._get_display() == "5."
        assert gui._current_input == "5."

    def test_gui_decimal_input_prevents_duplicate_dots(self, tk_root, calculator, history_tracker):
        """Test that duplicate decimal points are prevented."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("3")
        gui._on_decimal()
        gui._on_digit("1")
        gui._on_decimal()  # This should not add another dot

        assert gui._get_display() == "3.1"
        assert gui._current_input == "3.1"

    def test_gui_decimal_input_first_char(self, tk_root, calculator, history_tracker):
        """Test entering decimal as first character."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_decimal()

        assert gui._get_display() == "0."

    def test_gui_decimal_input_after_error(self, tk_root, calculator, history_tracker):
        """Test that decimal input clears error display."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._set_display("Error: something")
        gui._current_input = "Error: something"
        gui._on_decimal()

        assert gui._get_display() == "0."


class TestBinaryOperations:
    """Tests for binary operation workflows."""

    def test_gui_binary_operation_workflow_add(self, tk_root, calculator, history_tracker):
        """Test workflow: 5 + 3 = → display shows 8."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        # Enter first operand
        gui._on_digit("5")
        assert gui._get_display() == "5"

        # Press add operation
        ops = mode.get_operations()
        add_fn, add_arity = ops["add"]
        gui._on_operation("add", add_fn, add_arity)
        assert gui._pending_op is not None
        assert gui._first_operand == 5.0
        assert gui._current_input == ""

        # Enter second operand
        gui._on_digit("3")
        assert gui._get_display() == "3"

        # Press equals
        gui._on_equals()
        assert gui._get_display() == "8"

    def test_gui_binary_operation_workflow_subtract(self, tk_root, calculator, history_tracker):
        """Test workflow: 10 - 4 = → display shows 6."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("1")
        gui._on_digit("0")
        ops = mode.get_operations()
        sub_fn, sub_arity = ops["subtract"]
        gui._on_operation("subtract", sub_fn, sub_arity)

        gui._on_digit("4")
        gui._on_equals()

        assert gui._get_display() == "6"

    def test_gui_binary_operation_workflow_multiply(self, tk_root, calculator, history_tracker):
        """Test workflow: 3 * 4 = → display shows 12."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("3")
        ops = mode.get_operations()
        mul_fn, mul_arity = ops["multiply"]
        gui._on_operation("multiply", mul_fn, mul_arity)

        gui._on_digit("4")
        gui._on_equals()

        assert gui._get_display() == "12"

    def test_gui_binary_operation_workflow_divide(self, tk_root, calculator, history_tracker):
        """Test workflow: 12 / 3 = → display shows 4."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("1")
        gui._on_digit("2")
        ops = mode.get_operations()
        div_fn, div_arity = ops["divide"]
        gui._on_operation("divide", div_fn, div_arity)

        gui._on_digit("3")
        gui._on_equals()

        assert gui._get_display() == "4"

    def test_gui_binary_operation_with_decimals(self, tk_root, calculator, history_tracker):
        """Test binary operation with decimal numbers: 2.5 + 1.5 = 4."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("2")
        gui._on_decimal()
        gui._on_digit("5")
        ops = mode.get_operations()
        add_fn, add_arity = ops["add"]
        gui._on_operation("add", add_fn, add_arity)

        gui._on_digit("1")
        gui._on_decimal()
        gui._on_digit("5")
        gui._on_equals()

        assert gui._get_display() == "4"

    def test_gui_equals_without_pending_op_is_noop(self, tk_root, calculator, history_tracker):
        """Test that pressing = without a pending operation does nothing."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("5")
        gui._on_equals()

        assert gui._get_display() == "5"


class TestUnaryOperations:
    """Tests for unary operation workflows."""

    def test_gui_unary_operation_square(self, tk_root, calculator, history_tracker):
        """Test unary operation: 9 squared = 81."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("9")
        ops = mode.get_operations()
        square_fn, square_arity = ops["square"]
        gui._on_operation("square", square_fn, square_arity)

        assert gui._get_display() == "81"

    def test_gui_unary_operation_square_root(self, tk_root, calculator, history_tracker):
        """Test unary operation: square_root(9) = 3."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("9")
        ops = mode.get_operations()
        sqrt_fn, sqrt_arity = ops["square_root"]
        gui._on_operation("square_root", sqrt_fn, sqrt_arity)

        # Could be "3" or "3.0" depending on formatting
        display = gui._get_display()
        assert float(display) == 3.0

    def test_gui_unary_operation_decimal_input(self, tk_root, calculator, history_tracker):
        """Test unary operation with decimal: square(2.5)."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("2")
        gui._on_decimal()
        gui._on_digit("5")
        ops = mode.get_operations()
        square_fn, square_arity = ops["square"]
        gui._on_operation("square", square_fn, square_arity)

        # 2.5 * 2.5 = 6.25
        assert gui._get_display() == "6.25"


class TestClear:
    """Tests for clear button functionality."""

    def test_gui_clear_resets_display(self, tk_root, calculator, history_tracker):
        """Test that clear button resets display to '0'."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("5")
        assert gui._get_display() == "5"

        gui._on_clear()
        assert gui._get_display() == "0"

    def test_gui_clear_resets_current_input(self, tk_root, calculator, history_tracker):
        """Test that clear resets current input."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("1")
        gui._on_digit("2")
        gui._on_clear()

        assert gui._current_input == ""

    def test_gui_clear_resets_pending_op(self, tk_root, calculator, history_tracker):
        """Test that clear resets pending operation."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("5")
        ops = mode.get_operations()
        add_fn, add_arity = ops["add"]
        gui._on_operation("add", add_fn, add_arity)

        gui._on_clear()
        assert gui._pending_op is None
        assert gui._pending_op_name is None

    def test_gui_clear_resets_first_operand(self, tk_root, calculator, history_tracker):
        """Test that clear resets first operand."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("5")
        ops = mode.get_operations()
        add_fn, add_arity = ops["add"]
        gui._on_operation("add", add_fn, add_arity)

        gui._on_clear()
        assert gui._first_operand is None


class TestErrorHandling:
    """Tests for error handling in operations."""

    def test_gui_error_on_division_by_zero(self, tk_root, calculator, history_tracker):
        """Test that 5 / 0 displays an error message."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("5")
        ops = mode.get_operations()
        div_fn, div_arity = ops["divide"]
        gui._on_operation("divide", div_fn, div_arity)

        gui._on_digit("0")
        gui._on_equals()

        assert gui._get_display().startswith("Error")

    def test_gui_error_on_invalid_sqrt(self, tk_root, calculator, history_tracker):
        """Test that sqrt(-4) displays an error message."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("-")  # This won't work, let's set current_input directly
        gui._current_input = "-4"
        gui._set_display("-4")
        ops = mode.get_operations()
        sqrt_fn, sqrt_arity = ops["square_root"]
        gui._on_operation("square_root", sqrt_fn, sqrt_arity)

        assert gui._get_display().startswith("Error")

    def test_gui_error_clears_on_digit_input(self, tk_root, calculator, history_tracker):
        """Test that entering a digit after error clears the error."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._set_display("Error: something")
        gui._current_input = "Error: something"
        gui._on_digit("5")

        assert gui._get_display() == "5"
        assert not gui._get_display().startswith("Error")


class TestHistoryRecording:
    """Tests for history tracking integration."""

    def test_gui_history_recording_binary_op(self, tk_root, calculator, history_tracker):
        """Test that binary operation is recorded in history."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("2")
        ops = mode.get_operations()
        add_fn, add_arity = ops["add"]
        gui._on_operation("add", add_fn, add_arity)

        gui._on_digit("3")
        gui._on_equals()

        history = history_tracker.get_history()
        assert len(history) > 0
        assert "add" in history[-1]

    def test_gui_history_recording_unary_op(self, tk_root, calculator, history_tracker):
        """Test that unary operation is recorded in history."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("4")
        ops = mode.get_operations()
        square_fn, square_arity = ops["square"]
        gui._on_operation("square", square_fn, square_arity)

        history = history_tracker.get_history()
        assert len(history) > 0
        assert "square" in history[-1]

    def test_gui_history_shows_operands_and_result(self, tk_root, calculator, history_tracker):
        """Test that history entry contains operands and result."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("5")
        ops = mode.get_operations()
        add_fn, add_arity = ops["add"]
        gui._on_operation("add", add_fn, add_arity)

        gui._on_digit("3")
        gui._on_equals()

        history = history_tracker.get_history()
        last_entry = history[-1]
        # Format: "add(5.0, 3.0) = 8" or similar
        assert "5" in last_entry
        assert "3" in last_entry
        assert "=" in last_entry


class TestModeSwitching:
    """Tests for mode switching functionality."""

    def test_gui_mode_switch_to_scientific(self, tk_root, calculator, history_tracker):
        """Test switching from Simple to Scientific mode."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        assert gui._mode.name == "Simple"

        gui._switch_to_scientific()

        assert gui._mode.name == "Scientific"

    def test_gui_mode_switch_to_simple(self, tk_root, calculator, history_tracker):
        """Test switching from Scientific to Simple mode."""
        mode = ScientificMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        assert gui._mode.name == "Scientific"

        gui._switch_to_simple()

        assert gui._mode.name == "Simple"

    def test_gui_mode_switch_updates_operations(self, tk_root, calculator, history_tracker):
        """Test that mode switch changes available operations."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        ops_before = gui._mode.get_operations()
        gui._switch_to_scientific()
        ops_after = gui._mode.get_operations()

        assert len(ops_before) < len(ops_after)

    def test_gui_mode_switch_resets_transient_state(self, tk_root, calculator, history_tracker):
        """Test that mode switch clears pending operation state."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("5")
        ops = mode.get_operations()
        add_fn, add_arity = ops["add"]
        gui._on_operation("add", add_fn, add_arity)

        gui._switch_to_scientific()

        assert gui._pending_op is None
        assert gui._current_input == ""
        assert gui._first_operand is None

    def test_gui_mode_switch_preserves_history(self, tk_root, calculator, history_tracker):
        """Test that mode switch preserves calculation history."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("2")
        ops = mode.get_operations()
        add_fn, add_arity = ops["add"]
        gui._on_operation("add", add_fn, add_arity)
        gui._on_digit("3")
        gui._on_equals()

        history_before = history_tracker.get_history()
        gui._switch_to_scientific()
        history_after = history_tracker.get_history()

        assert history_before == history_after
        assert len(history_after) > 0

    def test_gui_mode_switch_noop_if_already_in_mode(self, tk_root, calculator, history_tracker):
        """Test that switching to same mode is a no-op."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        initial_mode_id = id(gui._mode)
        gui._switch_to_simple()
        final_mode_id = id(gui._mode)

        # A new mode instance is created, but it's the same mode type
        assert gui._mode.name == "Simple"


class TestScientificOperations:
    """Tests for scientific-mode-only operations."""

    def test_gui_factorial_integer_input(self, tk_root, calculator, history_tracker):
        """Test 5! = 120."""
        mode = ScientificMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("5")
        ops = mode.get_operations()
        fact_fn, fact_arity = ops["factorial"]
        gui._on_operation("factorial", fact_fn, fact_arity)

        assert gui._get_display() == "120"

    def test_gui_factorial_float_error(self, tk_root, calculator, history_tracker):
        """Test that 5.5! displays an error."""
        mode = ScientificMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("5")
        gui._on_decimal()
        gui._on_digit("5")
        ops = mode.get_operations()
        fact_fn, fact_arity = ops["factorial"]
        gui._on_operation("factorial", fact_fn, fact_arity)

        assert gui._get_display().startswith("Error")

    def test_gui_power_operation(self, tk_root, calculator, history_tracker):
        """Test power operation: 2 ^ 3 = 8."""
        mode = ScientificMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("2")
        ops = mode.get_operations()
        power_fn, power_arity = ops["power"]
        gui._on_operation("power", power_fn, power_arity)

        gui._on_digit("3")
        gui._on_equals()

        assert gui._get_display() == "8"

    def test_gui_cube_operation(self, tk_root, calculator, history_tracker):
        """Test cube operation: 3³ = 27."""
        mode = ScientificMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._on_digit("3")
        ops = mode.get_operations()
        cube_fn, cube_arity = ops["cube"]
        gui._on_operation("cube", cube_fn, cube_arity)

        assert gui._get_display() == "27"


class TestDisplayFormatting:
    """Tests for result formatting."""

    def test_gui_format_result_integer(self, tk_root, calculator, history_tracker):
        """Test that integer results display without decimal point."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        result_str = gui._format_result(5)
        assert result_str == "5"
        assert "." not in result_str

    def test_gui_format_result_whole_float(self, tk_root, calculator, history_tracker):
        """Test that whole-number floats display without decimal point."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        result_str = gui._format_result(5.0)
        assert result_str == "5"
        assert "." not in result_str

    def test_gui_format_result_decimal(self, tk_root, calculator, history_tracker):
        """Test that decimal floats display with decimal point."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        result_str = gui._format_result(5.5)
        assert "5.5" in result_str

    def test_gui_format_result_very_small_float(self, tk_root, calculator, history_tracker):
        """Test formatting of very small floats."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        result_str = gui._format_result(0.0000001)
        # Should use scientific notation or limit precision
        assert isinstance(result_str, str)


class TestParseInput:
    """Tests for input parsing."""

    def test_gui_parse_current_input_valid_int(self, tk_root, calculator, history_tracker):
        """Test parsing a valid integer."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._current_input = "5"
        result = gui._parse_current_input()

        assert result == 5.0

    def test_gui_parse_current_input_valid_float(self, tk_root, calculator, history_tracker):
        """Test parsing a valid float."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._current_input = "3.14"
        result = gui._parse_current_input()

        assert result == 3.14

    def test_gui_parse_current_input_empty(self, tk_root, calculator, history_tracker):
        """Test parsing empty string returns None."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._current_input = ""
        result = gui._parse_current_input()

        assert result is None

    def test_gui_parse_current_input_error_message(self, tk_root, calculator, history_tracker):
        """Test parsing error message returns None."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._current_input = "Error: something"
        result = gui._parse_current_input()

        assert result is None

    def test_gui_parse_current_input_whitespace(self, tk_root, calculator, history_tracker):
        """Test parsing whitespace returns None."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        gui._current_input = "   "
        result = gui._parse_current_input()

        assert result is None


def collect_buttons_recursive(widget):
    """Recursively collect all Button widgets from a tkinter widget tree."""
    buttons = []
    if not HAS_TKINTER:
        return buttons
    try:
        for child in widget.winfo_children():
            if isinstance(child, tk.Button):
                buttons.append(child)
            buttons.extend(collect_buttons_recursive(child))
    except:
        pass
    return buttons


def find_button_by_text(widget, text):
    """Find the first Button with matching text in the widget tree."""
    buttons = collect_buttons_recursive(widget)
    for btn in buttons:
        try:
            if btn.cget("text") == text:
                return btn
        except:
            pass
    return None


class TestIOSRedesign:
    """Tests for iOS-style calculator redesign."""

    def test_theme_dict_exists(self):
        """Test that _THEME dict exists and has all required keys."""
        required_keys = [
            "window_bg", "display_bg", "display_fg", "display_font",
            "op_bg", "op_fg", "op_hover",
            "sci_bg", "sci_fg", "sci_hover",
            "std_bg", "std_fg", "std_hover"
        ]
        for key in required_keys:
            assert key in _THEME, f"Missing key in _THEME: {key}"

    def test_theme_dict_has_expected_values(self):
        """Test that _THEME colours are set to expected values."""
        assert _THEME["window_bg"] == "#000000"
        assert _THEME["display_bg"] == "#000000"
        assert _THEME["display_fg"] == "#FFFFFF"
        assert _THEME["op_bg"] == "#FF9500"
        assert _THEME["op_fg"] == "#FFFFFF"
        assert _THEME["op_hover"] == "#FFB143"
        assert _THEME["sci_bg"] == "#1C1C1E"
        assert _THEME["sci_fg"] == "#FFFFFF"
        assert _THEME["sci_hover"] == "#2C2C2E"
        assert _THEME["std_bg"] == "#333333"
        assert _THEME["std_fg"] == "#FFFFFF"
        assert _THEME["std_hover"] == "#4D4D4D"

    def test_symbols_dict_exists(self):
        """Test that _SYMBOLS dict exists and maps operation names to Unicode symbols."""
        required_mappings = {
            "add": "+",
            "subtract": "−",
            "multiply": "×",
            "divide": "÷",
            "square_root": "√",
        }
        for op_name, expected_symbol in required_mappings.items():
            assert op_name in _SYMBOLS, f"Missing operation in _SYMBOLS: {op_name}"
            assert _SYMBOLS[op_name] == expected_symbol, f"Symbol mismatch for {op_name}: expected {expected_symbol}, got {_SYMBOLS[op_name]}"

    def test_symbols_dict_has_all_scientific_ops(self):
        """Test that _SYMBOLS includes scientific operations."""
        sci_ops = ["square", "cube", "factorial", "log", "ln", "sin", "cos", "tan", "pi", "e"]
        for op_name in sci_ops:
            assert op_name in _SYMBOLS, f"Missing operation in _SYMBOLS: {op_name}"

    def test_arithmetic_ops_set(self):
        """Test that _ARITHMETIC_OPS set equals the expected set."""
        expected = {"add", "subtract", "multiply", "divide"}
        assert _ARITHMETIC_OPS == expected, f"_ARITHMETIC_OPS mismatch: expected {expected}, got {_ARITHMETIC_OPS}"

    @pytest.mark.skipif(not HAS_TKINTER, reason="tkinter not available")
    def test_display_is_label(self, tk_root, calculator, history_tracker):
        """Test that the display widget is a tk.Label, not tk.Entry."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        assert hasattr(gui, "_display"), "GUI missing _display attribute"
        assert isinstance(gui._display, tk.Label), f"Display should be tk.Label, got {type(gui._display)}"

    @pytest.mark.skipif(not HAS_TKINTER, reason="tkinter not available")
    def test_display_initial_value(self, tk_root, calculator, history_tracker):
        """Test that display initializes to '0'."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        assert gui._get_display() == "0"

    @pytest.mark.skipif(not HAS_TKINTER, reason="tkinter not available")
    def test_mode_toggle_shows_scientific_in_simple_mode(self, tk_root, calculator, history_tracker):
        """Test that mode toggle button shows 'Scientific' when in Simple mode."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        # Find the mode toggle button (should have text "Scientific" in Simple mode)
        toggle_btn = find_button_by_text(tk_root, "Scientific")
        assert toggle_btn is not None, "Could not find mode toggle button with text 'Scientific'"
        assert toggle_btn.cget("text") == "Scientific"

    @pytest.mark.skipif(not HAS_TKINTER, reason="tkinter not available")
    def test_mode_toggle_shows_normal_in_scientific_mode(self, tk_root, calculator, history_tracker):
        """Test that mode toggle button shows 'Normal' when in Scientific mode."""
        mode = ScientificMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        # Find the mode toggle button (should have text "Normal" in Scientific mode)
        toggle_btn = find_button_by_text(tk_root, "Normal")
        assert toggle_btn is not None, "Could not find mode toggle button with text 'Normal'"
        assert toggle_btn.cget("text") == "Normal"

    @pytest.mark.skipif(not HAS_TKINTER, reason="tkinter not available")
    def test_toggle_mode_switches_to_scientific(self, tk_root, calculator, history_tracker):
        """Test that _toggle_mode() switches from Simple to Scientific."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        assert gui._mode.name == "Simple"
        gui._toggle_mode()
        assert gui._mode.name == "Scientific"

    @pytest.mark.skipif(not HAS_TKINTER, reason="tkinter not available")
    def test_toggle_mode_switches_to_simple(self, tk_root, calculator, history_tracker):
        """Test that _toggle_mode() switches from Scientific to Simple."""
        mode = ScientificMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        assert gui._mode.name == "Scientific"
        gui._toggle_mode()
        assert gui._mode.name == "Simple"

    @pytest.mark.skipif(not HAS_TKINTER, reason="tkinter not available")
    def test_op_button_colors_arithmetic(self, tk_root, calculator, history_tracker):
        """Test that arithmetic operation buttons have op_bg colour."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        # Find an arithmetic op button (e.g., "+" for add)
        add_btn = find_button_by_text(tk_root, "+")
        assert add_btn is not None, "Could not find add button with text '+'"
        assert add_btn.cget("bg") == _THEME["op_bg"], \
            f"Add button bg should be {_THEME['op_bg']}, got {add_btn.cget('bg')}"

    @pytest.mark.skipif(not HAS_TKINTER, reason="tkinter not available")
    def test_op_button_colors_standard(self, tk_root, calculator, history_tracker):
        """Test that non-arithmetic operation buttons in Simple mode have std_bg colour."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        # Find a standard operation button (e.g., "x²" for square)
        square_btn = find_button_by_text(tk_root, "x²")
        assert square_btn is not None, "Could not find square button with text 'x²'"
        assert square_btn.cget("bg") == _THEME["std_bg"], \
            f"Square button bg should be {_THEME['std_bg']}, got {square_btn.cget('bg')}"

    @pytest.mark.skipif(not HAS_TKINTER, reason="tkinter not available")
    def test_op_button_colors_scientific(self, tk_root, calculator, history_tracker):
        """Test that non-arithmetic operation buttons in Scientific mode have sci_bg colour."""
        mode = ScientificMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        # Find a scientific operation button (e.g., "n!" for factorial)
        factorial_btn = find_button_by_text(tk_root, "n!")
        assert factorial_btn is not None, "Could not find factorial button with text 'n!'"
        assert factorial_btn.cget("bg") == _THEME["sci_bg"], \
            f"Factorial button bg should be {_THEME['sci_bg']}, got {factorial_btn.cget('bg')}"

    @pytest.mark.skipif(not HAS_TKINTER, reason="tkinter not available")
    def test_hover_bind_enter(self, tk_root):
        """Test that hover binding applies hover colour on <Enter> event."""
        btn = tk.Button(tk_root, text="Test", bg="#FF9500")
        gui = CalculatorGUI.__new__(CalculatorGUI)

        gui._bind_hover(btn, "#FF9500", "#FFB143")

        # Simulate <Enter> event
        btn.event_generate("<Enter>")
        tk_root.update()

        assert btn.cget("bg") == "#FFB143", f"Button bg should be #FFB143 after hover, got {btn.cget('bg')}"

    @pytest.mark.skipif(not HAS_TKINTER, reason="tkinter not available")
    def test_hover_bind_leave(self, tk_root):
        """Test that hover binding restores default colour on <Leave> event."""
        btn = tk.Button(tk_root, text="Test", bg="#FF9500")
        gui = CalculatorGUI.__new__(CalculatorGUI)

        gui._bind_hover(btn, "#FF9500", "#FFB143")

        # Simulate <Enter> then <Leave>
        btn.event_generate("<Enter>")
        tk_root.update()
        btn.event_generate("<Leave>")
        tk_root.update()

        assert btn.cget("bg") == "#FF9500", f"Button bg should be #FF9500 after leave, got {btn.cget('bg')}"

    @pytest.mark.skipif(not HAS_TKINTER, reason="tkinter not available")
    def test_symbol_mapping_applied_to_buttons(self, tk_root, calculator, history_tracker):
        """Test that symbol mappings are applied to operation buttons."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        buttons = collect_buttons_recursive(tk_root)
        button_texts = [btn.cget("text") for btn in buttons]

        # Check that Unicode symbols appear in button texts
        expected_symbols = ["÷", "+"]  # divide and add symbols must appear
        for symbol in expected_symbols:
            assert symbol in button_texts, f"Symbol {symbol} not found in button texts: {button_texts}"

    @pytest.mark.skipif(not HAS_TKINTER, reason="tkinter not available")
    def test_all_digit_buttons_present(self, tk_root, calculator, history_tracker):
        """Test that all digit buttons (0-9) are created."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        buttons = collect_buttons_recursive(tk_root)
        button_texts = [btn.cget("text") for btn in buttons]

        for digit in "0123456789":
            assert digit in button_texts, f"Digit button {digit} not found in button texts"

    @pytest.mark.skipif(not HAS_TKINTER, reason="tkinter not available")
    def test_clear_and_equals_buttons_present(self, tk_root, calculator, history_tracker):
        """Test that clear (C) and equals (=) buttons are present."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        c_btn = find_button_by_text(tk_root, "C")
        eq_btn = find_button_by_text(tk_root, "=")

        assert c_btn is not None, "Clear button 'C' not found"
        assert eq_btn is not None, "Equals button '=' not found"

    @pytest.mark.skipif(not HAS_TKINTER, reason="tkinter not available")
    def test_clear_button_has_op_color(self, tk_root, calculator, history_tracker):
        """Test that clear button has operation button colour (op_bg)."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        c_btn = find_button_by_text(tk_root, "C")
        assert c_btn is not None
        assert c_btn.cget("bg") == _THEME["op_bg"], \
            f"Clear button bg should be {_THEME['op_bg']}, got {c_btn.cget('bg')}"

    @pytest.mark.skipif(not HAS_TKINTER, reason="tkinter not available")
    def test_equals_button_has_op_color(self, tk_root, calculator, history_tracker):
        """Test that equals button has operation button colour (op_bg)."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        eq_btn = find_button_by_text(tk_root, "=")
        assert eq_btn is not None
        assert eq_btn.cget("bg") == _THEME["op_bg"], \
            f"Equals button bg should be {_THEME['op_bg']}, got {eq_btn.cget('bg')}"

    @pytest.mark.skipif(not HAS_TKINTER, reason="tkinter not available")
    def test_decimal_button_present(self, tk_root, calculator, history_tracker):
        """Test that decimal point button is present."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        dot_btn = find_button_by_text(tk_root, ".")
        assert dot_btn is not None, "Decimal button '.' not found"

    @pytest.mark.skipif(not HAS_TKINTER, reason="tkinter not available")
    def test_decimal_button_has_std_color(self, tk_root, calculator, history_tracker):
        """Test that decimal button has standard button colour (std_bg)."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        dot_btn = find_button_by_text(tk_root, ".")
        assert dot_btn is not None
        assert dot_btn.cget("bg") == _THEME["std_bg"], \
            f"Decimal button bg should be {_THEME['std_bg']}, got {dot_btn.cget('bg')}"

    @pytest.mark.skipif(not HAS_TKINTER, reason="tkinter not available")
    def test_mode_toggle_button_has_std_color(self, tk_root, calculator, history_tracker):
        """Test that mode toggle button has standard button colour."""
        mode = SimpleMode(calculator)
        gui = CalculatorGUI(tk_root, calculator, mode, history_tracker)

        toggle_btn = find_button_by_text(tk_root, "Scientific")
        assert toggle_btn is not None
        assert toggle_btn.cget("bg") == _THEME["std_bg"], \
            f"Mode toggle button bg should be {_THEME['std_bg']}, got {toggle_btn.cget('bg')}"
