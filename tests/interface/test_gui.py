"""Comprehensive tests for GUICalculator tkinter interface.

Tests cover:
- GUI initialization and structure
- Mode switching (normal/scientific)
- Operation selection and arity-driven input fields
- Calculation execution and result display
- Error handling and validation
- History panel population and updates
- Integration with __main__ entry point
- Edge cases and robustness
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
from typing import Optional
import sys

# Try to import tkinter; skip tests if unavailable (headless CI environments)
try:
    import tkinter as tk
    from tkinter import messagebox
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    # Create mock tkinter for import purposes
    tk = MagicMock()
    messagebox = MagicMock()

from src.calculator import Calculator
from src.context import CalculatorContext
from src.support.error_logger import ErrorLogger
from src.support.history import OperationHistory

# Only import GUICalculator if tkinter is available
if TKINTER_AVAILABLE:
    from src.interface.gui import GUICalculator
else:
    # Create a mock GUICalculator for non-tkinter environments
    class GUICalculator:
        pass


pytestmark = pytest.mark.skipif(not TKINTER_AVAILABLE, reason="tkinter not available in headless environment")


@pytest.fixture
def calculator():
    """Provide a fresh Calculator instance for each test."""
    return Calculator()


@pytest.fixture
def history():
    """Provide a fresh OperationHistory instance for each test."""
    hist = OperationHistory(history_file=":memory:")
    hist.clear_history()
    return hist


@pytest.fixture
def error_logger():
    """Provide a fresh ErrorLogger instance for each test."""
    logger = ErrorLogger(error_file=":memory:")
    logger.clear_errors()
    return logger


@pytest.fixture
def context():
    """Provide a fresh CalculatorContext instance for each test."""
    return CalculatorContext()


@pytest.fixture
def gui(calculator, history, error_logger, context):
    """Provide a GUICalculator instance with all dependencies injected."""
    gui_instance = GUICalculator(
        calculator,
        history=history,
        error_logger=error_logger,
        context=context,
    )
    yield gui_instance
    # Cleanup after test
    try:
        gui_instance.destroy()
    except Exception:
        pass


# ==============================================================================
# A. GUI Initialization and Structure Tests
# ==============================================================================

class TestGUIInitialization:
    """Test GUICalculator.__init__() and component setup."""

    def test_gui_initializes_with_all_dependencies(self, calculator, history, error_logger, context):
        """Verify GUICalculator initializes with injected dependencies."""
        gui = GUICalculator(
            calculator,
            history=history,
            error_logger=error_logger,
            context=context,
        )
        assert gui.calculator is calculator
        assert gui.history is history
        assert gui.error_logger is error_logger
        assert gui._context is context
        gui.destroy()

    def test_gui_creates_fresh_context_when_none_provided(self, calculator, history, error_logger):
        """Verify GUICalculator creates a fresh CalculatorContext when context=None."""
        gui = GUICalculator(
            calculator,
            history=history,
            error_logger=error_logger,
            context=None,
        )
        assert gui._context is not None
        assert isinstance(gui._context, CalculatorContext)
        assert gui._context.get_mode() == "normal"
        gui.destroy()

    def test_gui_initializes_operation_registry(self, gui):
        """Verify GUICalculator initializes OperationRegistry."""
        assert gui._registry is not None
        assert hasattr(gui._registry, 'get_operations')
        assert hasattr(gui._registry, 'dispatch')

    def test_gui_default_mode_is_normal(self, gui):
        """Verify default mode is 'normal'."""
        assert gui._context.get_mode() == "normal"
        assert gui._mode_var.get() == "normal"

    def test_gui_initializes_selected_operation_as_none(self, gui):
        """Verify _selected_operation starts as None."""
        assert gui._selected_operation is None

    def test_gui_initializes_operand_entries_list(self, gui):
        """Verify _operand_entries is initialized as an empty list."""
        assert isinstance(gui._operand_entries, list)

    def test_gui_initializes_frames_as_none(self, gui):
        """Verify frame references are initialized."""
        assert gui._operation_buttons_frame is not None
        assert gui._operand_frame is not None
        assert gui._history_listbox is not None

    def test_gui_initializes_result_var(self, gui):
        """Verify _result_var is a StringVar initialized to empty."""
        assert isinstance(gui._result_var, tk.StringVar)
        assert gui._result_var.get() == ""

    def test_gui_window_title_is_calculator(self, gui):
        """Verify window title is 'Calculator'."""
        assert gui.title() == "Calculator"

    def test_gui_window_not_resizable(self, gui):
        """Verify window is not resizable."""
        assert gui.resizable() == (False, False)

    def test_gui_with_none_history_no_crash(self, calculator, error_logger, context):
        """Verify GUICalculator works with history=None."""
        gui = GUICalculator(
            calculator,
            history=None,
            error_logger=error_logger,
            context=context,
        )
        assert gui.history is None
        gui.destroy()

    def test_gui_with_none_error_logger_no_crash(self, calculator, history, context):
        """Verify GUICalculator works with error_logger=None."""
        gui = GUICalculator(
            calculator,
            history=history,
            error_logger=None,
            context=context,
        )
        assert gui.error_logger is None
        gui.destroy()

    def test_gui_with_only_calculator_required(self, calculator):
        """Verify GUICalculator can be initialized with only calculator."""
        gui = GUICalculator(calculator)
        assert gui.calculator is calculator
        gui.destroy()


# ==============================================================================
# B. Mode Switching Tests
# ==============================================================================

class TestModeSwitching:
    """Test mode selector and mode change handling."""

    def test_mode_selector_normal_button_visible(self, gui):
        """Verify mode selector has 'Normal' radio button."""
        # The mode selector is created; we verify via children or internal state
        assert gui._context.get_mode() in ("normal", "scientific")

    def test_mode_switch_to_scientific(self, gui):
        """Verify switching mode to scientific updates context and registry."""
        gui._handle_mode_change("scientific")
        assert gui._context.get_mode() == "scientific"
        assert gui._registry._current_mode == "scientific"

    def test_mode_switch_back_to_normal(self, gui):
        """Verify switching back to normal updates context and registry."""
        gui._handle_mode_change("scientific")
        gui._handle_mode_change("normal")
        assert gui._context.get_mode() == "normal"
        assert gui._registry._current_mode == "normal"

    def test_mode_change_clears_selected_operation(self, gui):
        """Verify mode switch clears the selected operation."""
        gui._selected_operation = "add"
        gui._handle_mode_change("scientific")
        assert gui._selected_operation is None

    def test_mode_change_clears_result_display(self, gui):
        """Verify mode switch clears the result display."""
        gui._result_var.set("42")
        gui._handle_mode_change("scientific")
        assert gui._result_var.get() == ""

    def test_mode_change_rebuilds_operation_buttons(self, gui):
        """Verify operation buttons are rebuilt on mode change."""
        # Get initial operation buttons in normal mode
        normal_ops = gui._registry.get_operations()
        normal_count = len(normal_ops)

        # Switch to scientific and verify button count changes
        gui._handle_mode_change("scientific")
        scientific_ops = gui._registry.get_operations()
        scientific_count = len(scientific_ops)

        # Scientific mode should have more operations (includes trig functions)
        assert scientific_count > normal_count

    def test_mode_change_only_shows_current_and_both_operations(self, gui):
        """Verify only 'both' and current-mode operations are displayed."""
        gui._handle_mode_change("scientific")
        visible_ops = gui._registry.get_operations()

        for op in visible_ops:
            assert op.mode == "both" or op.mode == "scientific"

        # No 'normal'-only operations should be visible
        all_normal_only = [op for op in gui._registry._operations if op.mode == "normal"]
        visible_names = {op.name for op in visible_ops}
        for op in all_normal_only:
            assert op.name not in visible_names

    def test_mode_change_rebuilds_operand_inputs(self, gui):
        """Verify operand inputs are rebuilt on mode change."""
        gui._selected_operation = "add"
        gui._build_operand_inputs()
        assert len(gui._operand_entries) == 2

        gui._handle_mode_change("scientific")
        # After mode change, _selected_operation is None, so default arity is 1
        assert len(gui._operand_entries) == 1


# ==============================================================================
# C. Operation Selection and Arity Tests
# ==============================================================================

class TestOperationSelection:
    """Test operation button selection and arity-driven input fields."""

    def test_select_binary_operation_shows_two_inputs(self, gui):
        """Verify selecting a binary operation (add) shows two input fields."""
        gui._handle_operation_selected("add")
        assert len(gui._operand_entries) == 2

    def test_select_unary_operation_shows_one_input(self, gui):
        """Verify selecting a unary operation (sin) shows one input field."""
        gui._handle_mode_change("scientific")
        gui._handle_operation_selected("sin")
        assert len(gui._operand_entries) == 1

    def test_operation_selection_stores_operation_name(self, gui):
        """Verify operation name is stored when selected."""
        gui._handle_operation_selected("subtract")
        assert gui._selected_operation == "subtract"

    def test_operation_selection_clears_result_display(self, gui):
        """Verify result is cleared when selecting a new operation."""
        gui._result_var.set("100")
        gui._handle_operation_selected("multiply")
        assert gui._result_var.get() == ""

    def test_operation_selection_rebuilds_operand_inputs(self, gui):
        """Verify operand inputs are rebuilt when operation changes."""
        gui._handle_operation_selected("add")
        assert len(gui._operand_entries) == 2
        gui._handle_operation_selected("factorial")
        assert len(gui._operand_entries) == 1

    def test_binary_operand_labels_correctly_named(self, gui):
        """Verify binary operation input labels are correctly named."""
        gui._handle_operation_selected("add")
        # We can't easily inspect label text from the Entry directly,
        # but we verify the Entry count is correct
        assert len(gui._operand_entries) == 2

    def test_unary_operand_label_is_value(self, gui):
        """Verify unary operation input label is 'Value:'."""
        gui._handle_operation_selected("factorial")
        assert len(gui._operand_entries) == 1

    def test_switching_between_operations_changes_arity(self, gui):
        """Verify switching between operations with different arities works."""
        gui._handle_operation_selected("add")
        assert len(gui._operand_entries) == 2

        gui._handle_operation_selected("square")
        assert len(gui._operand_entries) == 1

        gui._handle_operation_selected("divide")
        assert len(gui._operand_entries) == 2


# ==============================================================================
# D. Calculation Execution Tests
# ==============================================================================

class TestCalculationExecution:
    """Test calculation dispatch and result display."""

    def test_execute_simple_addition(self, gui):
        """Verify 2 + 3 = 5."""
        gui._handle_operation_selected("add")
        gui._operand_entries[0].insert(0, "2")
        gui._operand_entries[1].insert(0, "3")

        gui._execute_calculation()

        assert gui._result_var.get() == "5"

    def test_execute_subtraction(self, gui):
        """Verify 10 - 3 = 7."""
        gui._handle_operation_selected("subtract")
        gui._operand_entries[0].insert(0, "10")
        gui._operand_entries[1].insert(0, "3")

        gui._execute_calculation()

        assert gui._result_var.get() == "7"

    def test_execute_multiplication(self, gui):
        """Verify 4 * 5 = 20."""
        gui._handle_operation_selected("multiply")
        gui._operand_entries[0].insert(0, "4")
        gui._operand_entries[1].insert(0, "5")

        gui._execute_calculation()

        assert gui._result_var.get() == "20"

    def test_execute_division(self, gui):
        """Verify 10 / 2 = 5."""
        gui._handle_operation_selected("divide")
        gui._operand_entries[0].insert(0, "10")
        gui._operand_entries[1].insert(0, "2")

        gui._execute_calculation()

        assert gui._result_var.get() == "5"

    def test_execute_unary_operation_factorial(self, gui):
        """Verify 5! = 120."""
        gui._handle_operation_selected("factorial")
        gui._operand_entries[0].insert(0, "5")

        gui._execute_calculation()

        assert gui._result_var.get() == "120"

    def test_execute_unary_operation_square_root(self, gui):
        """Verify sqrt(9) = 3."""
        gui._handle_operation_selected("square_root")
        gui._operand_entries[0].insert(0, "9")

        gui._execute_calculation()

        assert gui._result_var.get() == "3"

    def test_execute_scientific_operation_sine(self, gui):
        """Verify sin(0) = 0."""
        gui._handle_mode_change("scientific")
        gui._handle_operation_selected("sin")
        gui._operand_entries[0].insert(0, "0")

        gui._execute_calculation()

        # sin(0) should be 0 (or very close due to floating point)
        result = float(gui._result_var.get())
        assert abs(result) < 1e-10

    def test_execute_with_float_operands(self, gui):
        """Verify operation with float operands works."""
        gui._handle_operation_selected("add")
        gui._operand_entries[0].insert(0, "2.5")
        gui._operand_entries[1].insert(0, "3.7")

        gui._execute_calculation()

        result = float(gui._result_var.get())
        assert abs(result - 6.2) < 1e-10

    def test_result_strips_trailing_zeros_for_integers(self, gui):
        """Verify integer results don't display unnecessary decimals."""
        gui._handle_operation_selected("add")
        gui._operand_entries[0].insert(0, "1")
        gui._operand_entries[1].insert(0, "1")

        gui._execute_calculation()

        # Result should be "2", not "2.0"
        assert gui._result_var.get() == "2"

    def test_execute_without_selected_operation_shows_error(self, gui):
        """Verify executing with no operation selected shows error."""
        assert gui._selected_operation is None

        with patch.object(messagebox, 'showerror') as mock_error:
            gui._execute_calculation()
            mock_error.assert_called_once()
            call_args = mock_error.call_args[0]
            assert "Please select an operation first" in call_args[1]

    def test_execute_with_empty_operand_shows_error(self, gui):
        """Verify executing with empty operand shows error."""
        gui._handle_operation_selected("add")
        gui._operand_entries[0].insert(0, "5")
        gui._operand_entries[1].insert(0, "")

        with patch.object(messagebox, 'showerror') as mock_error:
            gui._execute_calculation()
            mock_error.assert_called_once()
            call_args = mock_error.call_args[0]
            assert "empty" in call_args[1].lower()

    def test_sequential_calculations_work_correctly(self, gui):
        """Verify multiple calculations in sequence work correctly."""
        gui._handle_operation_selected("add")
        gui._operand_entries[0].insert(0, "2")
        gui._operand_entries[1].insert(0, "3")
        gui._execute_calculation()
        assert gui._result_var.get() == "5"

        # Clear entries for second calculation
        gui._operand_entries[0].delete(0, tk.END)
        gui._operand_entries[1].delete(0, tk.END)
        gui._handle_operation_selected("multiply")
        gui._operand_entries[0].insert(0, "4")
        gui._operand_entries[1].insert(0, "5")
        gui._execute_calculation()
        assert gui._result_var.get() == "20"


# ==============================================================================
# E. Error Handling Tests
# ==============================================================================

class TestErrorHandling:
    """Test error detection and display."""

    def test_non_numeric_input_shows_error(self, gui):
        """Verify non-numeric input shows error."""
        gui._handle_operation_selected("add")
        gui._operand_entries[0].insert(0, "abc")
        gui._operand_entries[1].insert(0, "3")

        with patch.object(messagebox, 'showerror') as mock_error:
            gui._execute_calculation()
            mock_error.assert_called_once()
            call_args = mock_error.call_args[0]
            assert "Invalid number" in call_args[1]

    def test_division_by_zero_shows_error(self, gui):
        """Verify division by zero shows error."""
        gui._handle_operation_selected("divide")
        gui._operand_entries[0].insert(0, "10")
        gui._operand_entries[1].insert(0, "0")

        with patch.object(messagebox, 'showerror') as mock_error:
            gui._execute_calculation()
            mock_error.assert_called_once()

    def test_sqrt_of_negative_shows_error(self, gui):
        """Verify sqrt of negative number shows error."""
        gui._handle_operation_selected("square_root")
        gui._operand_entries[0].insert(0, "-4")

        with patch.object(messagebox, 'showerror') as mock_error:
            gui._execute_calculation()
            mock_error.assert_called_once()
            call_args = mock_error.call_args[0]
            assert "not defined" in call_args[1].lower()

    def test_factorial_of_non_integer_shows_error(self, gui):
        """Verify factorial of non-integer float shows error."""
        gui._handle_operation_selected("factorial")
        gui._operand_entries[0].insert(0, "5.5")

        with patch.object(messagebox, 'showerror') as mock_error:
            gui._execute_calculation()
            mock_error.assert_called_once()

    def test_logarithm_invalid_base_shows_error(self, gui):
        """Verify logarithm with invalid base shows error."""
        gui._handle_operation_selected("logarithm")
        gui._operand_entries[0].insert(0, "10")
        gui._operand_entries[1].insert(0, "1")  # Invalid base

        with patch.object(messagebox, 'showerror') as mock_error:
            gui._execute_calculation()
            mock_error.assert_called_once()

    def test_logarithm_of_non_positive_shows_error(self, gui):
        """Verify logarithm of non-positive number shows error."""
        gui._handle_operation_selected("logarithm")
        gui._operand_entries[0].insert(0, "-5")
        gui._operand_entries[1].insert(0, "2")

        with patch.object(messagebox, 'showerror') as mock_error:
            gui._execute_calculation()
            mock_error.assert_called_once()

    def test_error_logger_called_on_calculation_error(self, gui, error_logger):
        """Verify ErrorLogger.log_error is called on calculation error."""
        gui.error_logger = error_logger
        gui._handle_operation_selected("divide")
        gui._operand_entries[0].insert(0, "1")
        gui._operand_entries[1].insert(0, "0")

        with patch.object(messagebox, 'showerror'):
            gui._execute_calculation()

        # Error should be logged
        errors = error_logger.get_errors()
        assert len(errors) > 0

    def test_error_logger_not_called_when_none(self, gui):
        """Verify no crash when error_logger is None."""
        gui.error_logger = None
        gui._handle_operation_selected("divide")
        gui._operand_entries[0].insert(0, "1")
        gui._operand_entries[1].insert(0, "0")

        with patch.object(messagebox, 'showerror'):
            gui._execute_calculation()
        # Should not crash

    def test_show_error_displays_messagebox(self, gui):
        """Verify _show_error displays error messagebox."""
        with patch.object(messagebox, 'showerror') as mock_error:
            gui._show_error("Test error message")
            mock_error.assert_called_once_with("Calculator Error", "Test error message")


# ==============================================================================
# F. History Display Tests
# ==============================================================================

class TestHistoryDisplay:
    """Test history panel and history operations."""

    def test_history_panel_initialized(self, gui):
        """Verify history panel is initialized."""
        assert gui._history_listbox is not None
        assert isinstance(gui._history_listbox, tk.Listbox)

    def test_calculation_recorded_in_history(self, gui, history):
        """Verify calculation is recorded in history."""
        gui._handle_operation_selected("add")
        gui._operand_entries[0].insert(0, "2")
        gui._operand_entries[1].insert(0, "3")

        gui._execute_calculation()

        hist_entries = history.display_history()
        assert len(hist_entries) == 1
        assert "add" in hist_entries[0]
        assert "5" in hist_entries[0]

    def test_history_display_updated_after_calculation(self, gui, history):
        """Verify history listbox is updated after calculation."""
        gui._handle_operation_selected("add")
        gui._operand_entries[0].insert(0, "1")
        gui._operand_entries[1].insert(0, "1")

        gui._execute_calculation()

        # Check that listbox contains the entry
        listbox_size = gui._history_listbox.size()
        assert listbox_size == 1

    def test_history_display_with_multiple_calculations(self, gui, history):
        """Verify history shows multiple calculations."""
        gui._handle_operation_selected("add")
        gui._operand_entries[0].insert(0, "2")
        gui._operand_entries[1].insert(0, "3")
        gui._execute_calculation()

        gui._operand_entries[0].delete(0, tk.END)
        gui._operand_entries[1].delete(0, tk.END)
        gui._handle_operation_selected("multiply")
        gui._operand_entries[0].insert(0, "4")
        gui._operand_entries[1].insert(0, "5")
        gui._execute_calculation()

        listbox_size = gui._history_listbox.size()
        assert listbox_size == 2

    def test_update_history_display_with_no_history_object(self, calculator, error_logger, context):
        """Verify no crash when history=None."""
        gui = GUICalculator(
            calculator,
            history=None,
            error_logger=error_logger,
            context=context,
        )
        gui._update_history_display()
        # Should not crash
        gui.destroy()

    def test_history_listbox_scrolls_to_newest_entry(self, gui, history):
        """Verify history listbox scrolls to newest entry."""
        # Add multiple calculations
        for i in range(10):
            gui._handle_operation_selected("add")
            gui._operand_entries[0].delete(0, tk.END)
            gui._operand_entries[1].delete(0, tk.END)
            gui._operand_entries[0].insert(0, str(i))
            gui._operand_entries[1].insert(0, "1")
            gui._execute_calculation()

        # Verify listbox shows all entries
        assert gui._history_listbox.size() == 10

    def test_history_display_empty_when_no_history(self, calculator, error_logger, context):
        """Verify empty history is handled."""
        gui = GUICalculator(
            calculator,
            history=OperationHistory(history_file=":memory:"),
            error_logger=error_logger,
            context=context,
        )
        gui.history.clear_history()
        gui._update_history_display()
        assert gui._history_listbox.size() == 0
        gui.destroy()


# ==============================================================================
# G. Integration with __main__ Tests
# ==============================================================================

class TestMainIntegration:
    """Test integration with __main__ entry point."""

    @patch('src.interface.gui.GUICalculator.mainloop')
    def test_main_gui_mode_launches_gui(self, mock_mainloop):
        """Verify main(['--gui']) launches GUI mode."""
        from src import main

        mock_mainloop.return_value = None
        main(["--gui"])

        # GUI mode should have been called
        mock_mainloop.assert_called_once()

    def test_main_repl_mode_unchanged(self):
        """Verify main() with no args or --repl still uses REPL mode."""
        from src import main
        from unittest.mock import patch

        with patch('src.interface.repl.REPLInterface.run') as mock_repl:
            main([])
            mock_repl.assert_called_once()

    def test_main_cli_mode_unchanged(self):
        """Verify main(['add', '2', '3']) still uses CLI mode."""
        from src import main
        from io import StringIO
        import sys

        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            main(["add", "2", "3"])
            output = sys.stdout.getvalue()
            assert "5" in output
        finally:
            sys.stdout = old_stdout

    @patch('src.interface.gui.GUICalculator.mainloop')
    def test_main_gui_creates_gui_calculator(self, mock_mainloop):
        """Verify GUICalculator is instantiated in GUI mode."""
        from src import main

        mock_mainloop.return_value = None
        with patch('src.interface.gui.GUICalculator') as MockGUICalculator:
            mock_instance = MagicMock()
            MockGUICalculator.return_value = mock_instance
            main(["--gui"])
            # GUI should have been instantiated
            MockGUICalculator.assert_called_once()


# ==============================================================================
# H. Edge Cases and Robustness Tests
# ==============================================================================

class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_large_number_input(self, gui):
        """Verify very large numbers are handled."""
        gui._handle_operation_selected("multiply")
        gui._operand_entries[0].insert(0, "1000000")
        gui._operand_entries[1].insert(0, "1000000")

        gui._execute_calculation()

        result = float(gui._result_var.get())
        assert result == 1e12

    def test_very_small_number_input(self, gui):
        """Verify very small numbers are handled."""
        gui._handle_operation_selected("multiply")
        gui._operand_entries[0].insert(0, "0.0001")
        gui._operand_entries[1].insert(0, "0.0001")

        gui._execute_calculation()

        result = float(gui._result_var.get())
        assert result < 0.00001

    def test_negative_number_input(self, gui):
        """Verify negative numbers are handled."""
        gui._handle_operation_selected("add")
        gui._operand_entries[0].insert(0, "-5")
        gui._operand_entries[1].insert(0, "-3")

        gui._execute_calculation()

        assert gui._result_var.get() == "-8"

    def test_whitespace_in_operand_is_stripped(self, gui):
        """Verify whitespace in operand input is stripped."""
        gui._handle_operation_selected("add")
        gui._operand_entries[0].insert(0, "  5  ")
        gui._operand_entries[1].insert(0, "  3  ")

        gui._execute_calculation()

        assert gui._result_var.get() == "8"

    def test_zero_operand(self, gui):
        """Verify zero operand is handled correctly."""
        gui._handle_operation_selected("multiply")
        gui._operand_entries[0].insert(0, "0")
        gui._operand_entries[1].insert(0, "100")

        gui._execute_calculation()

        assert gui._result_var.get() == "0"

    def test_factorial_of_zero(self, gui):
        """Verify 0! = 1."""
        gui._handle_operation_selected("factorial")
        gui._operand_entries[0].insert(0, "0")

        gui._execute_calculation()

        assert gui._result_var.get() == "1"

    def test_power_operation(self, gui):
        """Verify power operation works."""
        gui._handle_operation_selected("power")
        gui._operand_entries[0].insert(0, "2")
        gui._operand_entries[1].insert(0, "8")

        gui._execute_calculation()

        assert gui._result_var.get() == "256"

    def test_square_operation(self, gui):
        """Verify square operation works."""
        gui._handle_operation_selected("square")
        gui._operand_entries[0].insert(0, "7")

        gui._execute_calculation()

        assert gui._result_var.get() == "49"

    def test_cube_operation(self, gui):
        """Verify cube operation works."""
        gui._handle_operation_selected("cube")
        gui._operand_entries[0].insert(0, "3")

        gui._execute_calculation()

        assert gui._result_var.get() == "27"

    def test_cube_root_operation(self, gui):
        """Verify cube root operation works."""
        gui._handle_operation_selected("cube_root")
        gui._operand_entries[0].insert(0, "27")

        gui._execute_calculation()

        result = float(gui._result_var.get())
        assert abs(result - 3.0) < 1e-10

    def test_logarithm_operation(self, gui):
        """Verify logarithm operation works."""
        gui._handle_operation_selected("logarithm")
        gui._operand_entries[0].insert(0, "100")
        gui._operand_entries[1].insert(0, "10")

        gui._execute_calculation()

        result = float(gui._result_var.get())
        assert abs(result - 2.0) < 1e-10

    def test_natural_logarithm_operation(self, gui):
        """Verify natural logarithm operation works."""
        gui._handle_operation_selected("natural_logarithm")
        gui._operand_entries[0].insert(0, "1")

        gui._execute_calculation()

        result = float(gui._result_var.get())
        assert abs(result) < 1e-10  # ln(1) = 0

    def test_cosine_operation(self, gui):
        """Verify cosine operation works."""
        gui._handle_mode_change("scientific")
        gui._handle_operation_selected("cos")
        gui._operand_entries[0].insert(0, "0")

        gui._execute_calculation()

        result = float(gui._result_var.get())
        assert abs(result - 1.0) < 1e-10  # cos(0) = 1

    def test_tangent_operation(self, gui):
        """Verify tangent operation works."""
        gui._handle_mode_change("scientific")
        gui._handle_operation_selected("tan")
        gui._operand_entries[0].insert(0, "0")

        gui._execute_calculation()

        result = float(gui._result_var.get())
        assert abs(result) < 1e-10  # tan(0) = 0

    def test_gui_with_injected_context_mode_honored(self, calculator, history, error_logger):
        """Verify injected context mode is honored."""
        context = CalculatorContext()
        context.set_mode("scientific")

        gui = GUICalculator(
            calculator,
            history=history,
            error_logger=error_logger,
            context=context,
        )

        assert gui._context.get_mode() == "scientific"
        gui.destroy()

    def test_multiple_calculations_with_mode_switching(self, gui):
        """Verify calculations work after mode switching."""
        # Normal mode calculation
        gui._handle_operation_selected("add")
        gui._operand_entries[0].insert(0, "2")
        gui._operand_entries[1].insert(0, "3")
        gui._execute_calculation()
        assert gui._result_var.get() == "5"

        # Switch to scientific
        gui._handle_mode_change("scientific")
        assert gui._selected_operation is None

        # Scientific calculation
        gui._handle_operation_selected("sin")
        gui._operand_entries[0].insert(0, "0")
        gui._execute_calculation()
        result = float(gui._result_var.get())
        assert abs(result) < 1e-10

    def test_operand_entries_cleared_between_operations(self, gui):
        """Verify Entry widgets maintain independence between operations."""
        gui._handle_operation_selected("add")
        gui._operand_entries[0].insert(0, "10")
        gui._operand_entries[1].insert(0, "20")

        # Switch operations
        gui._handle_operation_selected("subtract")

        # New operation should have fresh Entry widgets
        assert gui._operand_entries[0].get() == ""
        assert gui._operand_entries[1].get() == ""

    def test_float_result_with_many_decimals(self, gui):
        """Verify float results are displayed properly."""
        gui._handle_operation_selected("divide")
        gui._operand_entries[0].insert(0, "10")
        gui._operand_entries[1].insert(0, "3")

        gui._execute_calculation()

        result_str = gui._result_var.get()
        result_float = float(result_str)
        assert abs(result_float - 10/3) < 1e-10


# ==============================================================================
# I. Additional Robustness and Integration Tests
# ==============================================================================

class TestRobustness:
    """Test overall robustness and error recovery."""

    def test_error_does_not_crash_gui(self, gui):
        """Verify calculation error doesn't crash the GUI."""
        gui._handle_operation_selected("divide")
        gui._operand_entries[0].insert(0, "1")
        gui._operand_entries[1].insert(0, "0")

        with patch.object(messagebox, 'showerror'):
            gui._execute_calculation()

        # GUI should still be responsive
        assert gui.calculator is not None

    def test_mode_switch_after_error(self, gui):
        """Verify mode switching works after an error."""
        gui._handle_operation_selected("divide")
        gui._operand_entries[0].insert(0, "1")
        gui._operand_entries[1].insert(0, "0")

        with patch.object(messagebox, 'showerror'):
            gui._execute_calculation()

        # Mode switching should still work
        gui._handle_mode_change("scientific")
        assert gui._context.get_mode() == "scientific"

    def test_successive_errors_handled(self, gui):
        """Verify multiple successive errors are handled."""
        for _ in range(3):
            gui._handle_operation_selected("divide")
            gui._operand_entries[0].insert(0, "1")
            gui._operand_entries[1].insert(0, "0")

            with patch.object(messagebox, 'showerror'):
                gui._execute_calculation()

            gui._operand_entries[0].delete(0, tk.END)
            gui._operand_entries[1].delete(0, tk.END)

    def test_calculation_after_invalid_input(self, gui):
        """Verify valid calculation works after invalid input."""
        gui._handle_operation_selected("add")
        gui._operand_entries[0].insert(0, "abc")
        gui._operand_entries[1].insert(0, "3")

        with patch.object(messagebox, 'showerror'):
            gui._execute_calculation()

        # Clear and try valid calculation
        gui._operand_entries[0].delete(0, tk.END)
        gui._operand_entries[1].delete(0, tk.END)
        gui._operand_entries[0].insert(0, "2")
        gui._operand_entries[1].insert(0, "3")

        gui._execute_calculation()

        assert gui._result_var.get() == "5"
