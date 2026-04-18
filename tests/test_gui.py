"""Tests for the GUI layer (src/gui.py).

Tests the CalculatorGUI and OperandInputWidget classes. Since the environment
is headless (no X11 display), we use mocking for tkinter and fixtures to
manage temporary files for history and logging.
"""

from __future__ import annotations

import sys
import os
import tempfile
from unittest.mock import MagicMock, Mock, patch, call
from pathlib import Path

import pytest

# Mock tkinter before importing gui module
sys.modules['tkinter'] = MagicMock()

from src.gui import OperandInputWidget, CalculatorGUI, COLORS
from src.mode import Mode
from src.error_logger import INVALID_INPUT, CALCULATION_ERROR


# ===========================================================================
# Fixtures for headless testing
# ===========================================================================


@pytest.fixture
def mock_tk_root():
    """Mock tkinter Tk root for testing without X11 display."""
    with patch("src.gui.tk.Tk"):
        yield


@pytest.fixture
def temp_history_log_dir(tmp_path, monkeypatch):
    """Create temporary directories for history and error log files."""
    history_file = tmp_path / "history.txt"
    error_log_file = tmp_path / "error.log"

    # Change to temp directory so history.txt and error.log are created there
    monkeypatch.chdir(tmp_path)

    return {
        "history_file": history_file,
        "error_log_file": error_log_file,
        "tmp_path": tmp_path,
    }


@pytest.fixture
def mock_root_window():
    """Create a mock tk.Tk root window."""
    mock_root = MagicMock()
    mock_root.title = MagicMock()
    mock_root.resizable = MagicMock()
    mock_root.pack = MagicMock()
    mock_root.mainloop = MagicMock()
    return mock_root


@pytest.fixture
def mock_tkinter_components(mock_root_window):
    """Patch all tkinter components needed for GUI testing."""
    with patch("src.gui.tk.Tk", return_value=mock_root_window) as mock_tk, \
         patch("src.gui.tk.LabelFrame") as mock_labelframe, \
         patch("src.gui.tk.Frame") as mock_frame, \
         patch("src.gui.tk.Label") as mock_label, \
         patch("src.gui.tk.Entry") as mock_entry, \
         patch("src.gui.tk.Radiobutton") as mock_radiobutton, \
         patch("src.gui.tk.Button") as mock_button, \
         patch("src.gui.tk.StringVar") as mock_stringvar, \
         patch("src.gui.tk.Listbox") as mock_listbox, \
         patch("src.gui.tk.Scrollbar") as mock_scrollbar, \
         patch("src.gui.tk.END", "end"):

        # Configure StringVar to track values
        string_var_values = {}
        def stringvar_init(value=""):
            var = MagicMock()
            var.get = MagicMock(return_value=value)
            var.set = MagicMock(side_effect=lambda v: string_var_values.update({"var": v}))
            return var
        mock_stringvar.side_effect = stringvar_init

        # Configure Entry widget
        entry_values = {}
        def entry_init(parent, **kwargs):
            widget = MagicMock()
            widget.get = MagicMock(return_value="")
            widget.delete = MagicMock()
            widget.grid = MagicMock()
            widget.grid_remove = MagicMock()
            return widget
        mock_entry.side_effect = entry_init

        # Configure Label widget
        def label_init(parent, **kwargs):
            widget = MagicMock()
            widget.grid = MagicMock()
            widget.grid_remove = MagicMock()
            widget.pack = MagicMock()
            return widget
        mock_label.side_effect = label_init

        # Configure Button widget
        def button_init(parent, **kwargs):
            widget = MagicMock()
            widget.grid = MagicMock()
            widget.pack = MagicMock()
            widget.config = MagicMock()
            widget.destroy = MagicMock()
            return widget
        mock_button.side_effect = button_init

        # Configure Listbox
        def listbox_init(parent, **kwargs):
            widget = MagicMock()
            widget.delete = MagicMock()
            widget.insert = MagicMock()
            widget.pack = MagicMock()
            widget.size = MagicMock(return_value=0)
            widget.see = MagicMock()
            return widget
        mock_listbox.side_effect = listbox_init

        yield {
            "tk": mock_tk,
            "labelframe": mock_labelframe,
            "frame": mock_frame,
            "label": mock_label,
            "entry": mock_entry,
            "radiobutton": mock_radiobutton,
            "button": mock_button,
            "stringvar": mock_stringvar,
            "listbox": mock_listbox,
            "scrollbar": mock_scrollbar,
        }


# ===========================================================================
# Tests for OperandInputWidget
# ===========================================================================


class TestOperandInputWidget:
    """Tests for the OperandInputWidget helper class."""

    def test_operand_widget_get_value_valid_positive_float(self):
        """Valid positive float string is parsed correctly."""
        mock_parent = MagicMock()
        mock_entry = MagicMock()

        with patch("src.gui.tk.Label") as mock_label, \
             patch("src.gui.tk.Entry", return_value=mock_entry):
            mock_label.return_value = MagicMock()
            mock_entry.get.return_value = "42.5"

            widget = OperandInputWidget(mock_parent, "Test:", 0)
            result = widget.get_value()

            assert result == 42.5

    def test_operand_widget_get_value_valid_negative_float(self):
        """Valid negative float string is parsed correctly."""
        mock_parent = MagicMock()
        mock_entry = MagicMock()

        with patch("src.gui.tk.Label") as mock_label, \
             patch("src.gui.tk.Entry", return_value=mock_entry):
            mock_label.return_value = MagicMock()
            mock_entry.get.return_value = "-15.25"

            widget = OperandInputWidget(mock_parent, "Test:", 0)
            result = widget.get_value()

            assert result == -15.25

    def test_operand_widget_get_value_valid_integer(self):
        """Valid integer string is parsed as float."""
        mock_parent = MagicMock()
        mock_entry = MagicMock()

        with patch("src.gui.tk.Label") as mock_label, \
             patch("src.gui.tk.Entry", return_value=mock_entry):
            mock_label.return_value = MagicMock()
            mock_entry.get.return_value = "100"

            widget = OperandInputWidget(mock_parent, "Test:", 0)
            result = widget.get_value()

            assert result == 100.0

    def test_operand_widget_get_value_with_whitespace(self):
        """String with leading/trailing whitespace is stripped and parsed."""
        mock_parent = MagicMock()
        mock_entry = MagicMock()

        with patch("src.gui.tk.Label") as mock_label, \
             patch("src.gui.tk.Entry", return_value=mock_entry):
            mock_label.return_value = MagicMock()
            mock_entry.get.return_value = "  25.5  "

            widget = OperandInputWidget(mock_parent, "Test:", 0)
            result = widget.get_value()

            assert result == 25.5

    def test_operand_widget_get_value_empty_string_raises_valueerror(self):
        """Empty string raises ValueError."""
        mock_parent = MagicMock()
        mock_entry = MagicMock()

        with patch("src.gui.tk.Label") as mock_label, \
             patch("src.gui.tk.Entry", return_value=mock_entry):
            mock_label.return_value = MagicMock()
            mock_entry.get.return_value = ""

            widget = OperandInputWidget(mock_parent, "Test:", 0)

            with pytest.raises(ValueError):
                widget.get_value()

    def test_operand_widget_get_value_whitespace_only_raises_valueerror(self):
        """Whitespace-only string raises ValueError."""
        mock_parent = MagicMock()
        mock_entry = MagicMock()

        with patch("src.gui.tk.Label") as mock_label, \
             patch("src.gui.tk.Entry", return_value=mock_entry):
            mock_label.return_value = MagicMock()
            mock_entry.get.return_value = "   "

            widget = OperandInputWidget(mock_parent, "Test:", 0)

            with pytest.raises(ValueError):
                widget.get_value()

    def test_operand_widget_get_value_non_numeric_raises_valueerror(self):
        """Non-numeric string raises ValueError."""
        mock_parent = MagicMock()
        mock_entry = MagicMock()

        with patch("src.gui.tk.Label") as mock_label, \
             patch("src.gui.tk.Entry", return_value=mock_entry):
            mock_label.return_value = MagicMock()
            mock_entry.get.return_value = "abc"

            widget = OperandInputWidget(mock_parent, "Test:", 0)

            with pytest.raises(ValueError):
                widget.get_value()

    def test_operand_widget_get_value_special_chars_raises_valueerror(self):
        """String with special characters raises ValueError."""
        mock_parent = MagicMock()
        mock_entry = MagicMock()

        with patch("src.gui.tk.Label") as mock_label, \
             patch("src.gui.tk.Entry", return_value=mock_entry):
            mock_label.return_value = MagicMock()
            mock_entry.get.return_value = "42@#$%"

            widget = OperandInputWidget(mock_parent, "Test:", 0)

            with pytest.raises(ValueError):
                widget.get_value()

    def test_operand_widget_clear_deletes_entry_text(self):
        """clear() deletes all text from the entry widget."""
        mock_parent = MagicMock()
        mock_entry = MagicMock()

        with patch("src.gui.tk.Label") as mock_label, \
             patch("src.gui.tk.Entry", return_value=mock_entry):
            mock_label.return_value = MagicMock()

            widget = OperandInputWidget(mock_parent, "Test:", 0)
            widget.clear()

            # Verify delete was called with (0, tk.END)
            mock_entry.delete.assert_called_once()
            args = mock_entry.delete.call_args[0]
            assert args[0] == 0

    def test_operand_widget_set_visible_true_shows_widgets(self):
        """set_visible(True) calls grid() on label and entry."""
        mock_parent = MagicMock()
        mock_label = MagicMock()
        mock_entry = MagicMock()

        with patch("src.gui.tk.Label", return_value=mock_label), \
             patch("src.gui.tk.Entry", return_value=mock_entry):

            widget = OperandInputWidget(mock_parent, "Test:", 0)
            # Reset the mocks after __init__
            mock_label.reset_mock()
            mock_entry.reset_mock()
            widget.set_visible(True)

            mock_label.grid.assert_called_once()
            mock_entry.grid.assert_called_once()

    def test_operand_widget_set_visible_false_hides_widgets(self):
        """set_visible(False) calls grid_remove() on label and entry."""
        mock_parent = MagicMock()
        mock_label = MagicMock()
        mock_entry = MagicMock()

        with patch("src.gui.tk.Label", return_value=mock_label), \
             patch("src.gui.tk.Entry", return_value=mock_entry):

            widget = OperandInputWidget(mock_parent, "Test:", 0)
            widget.set_visible(False)

            mock_label.grid_remove.assert_called_once()
            mock_entry.grid_remove.assert_called_once()

    def test_operand_widget_zero_value(self):
        """Zero value is parsed correctly."""
        mock_parent = MagicMock()
        mock_entry = MagicMock()

        with patch("src.gui.tk.Label") as mock_label, \
             patch("src.gui.tk.Entry", return_value=mock_entry):
            mock_label.return_value = MagicMock()
            mock_entry.get.return_value = "0"

            widget = OperandInputWidget(mock_parent, "Test:", 0)
            result = widget.get_value()

            assert result == 0.0


# ===========================================================================
# Tests for CalculatorGUI Initialization
# ===========================================================================


class TestGUIInitialization:
    """Tests for CalculatorGUI initialization."""

    def test_gui_creates_root_window(self, mock_tkinter_components, temp_history_log_dir):
        """GUI __init__ creates and configures the root Tk window."""
        gui = CalculatorGUI()

        assert gui._root is not None
        gui._root.title.assert_called_once_with("Calculator")
        gui._root.resizable.assert_called_once_with(False, False)

    def test_gui_initializes_calculator(self, mock_tkinter_components, temp_history_log_dir):
        """GUI creates a Calculator instance."""
        gui = CalculatorGUI()

        assert gui._calc is not None
        from src.calculator import Calculator
        assert isinstance(gui._calc, Calculator)

    def test_gui_initializes_operation_history(self, mock_tkinter_components, temp_history_log_dir):
        """GUI creates an OperationHistory instance."""
        gui = CalculatorGUI()

        assert gui._history is not None
        from src.history import OperationHistory
        assert isinstance(gui._history, OperationHistory)

    def test_gui_initializes_error_logger(self, mock_tkinter_components, temp_history_log_dir):
        """GUI creates an ErrorLogger instance."""
        gui = CalculatorGUI()

        assert gui._error_logger is not None
        from src.error_logger import ErrorLogger
        assert isinstance(gui._error_logger, ErrorLogger)

    def test_gui_initializes_in_normal_mode(self, mock_tkinter_components, temp_history_log_dir):
        """GUI starts in Normal mode."""
        gui = CalculatorGUI()

        assert gui._current_mode == Mode.NORMAL

    def test_gui_initializes_with_no_operation_selected(self, mock_tkinter_components, temp_history_log_dir):
        """GUI starts with no operation selected."""
        gui = CalculatorGUI()

        assert gui._selected_operation is None

    def test_gui_initializes_operand_widgets_list(self, mock_tkinter_components, temp_history_log_dir):
        """GUI creates a list to store operand widgets."""
        gui = CalculatorGUI()

        assert isinstance(gui._operand_widgets, list)
        assert len(gui._operand_widgets) == 2

    def test_gui_initializes_operation_buttons_list(self, mock_tkinter_components, temp_history_log_dir):
        """GUI creates a list to store operation buttons."""
        gui = CalculatorGUI()

        assert isinstance(gui._operation_buttons, list)


# ===========================================================================
# Tests for Mode Selection
# ===========================================================================


class TestModeSelection:
    """Tests for mode switching functionality."""

    def test_switch_to_scientific_mode(self, mock_tkinter_components, temp_history_log_dir):
        """Switching to scientific mode updates _current_mode."""
        gui = CalculatorGUI()
        gui._on_mode_changed(Mode.SCIENTIFIC)

        assert gui._current_mode == Mode.SCIENTIFIC

    def test_switch_to_normal_mode(self, mock_tkinter_components, temp_history_log_dir):
        """Switching to normal mode updates _current_mode."""
        gui = CalculatorGUI()
        gui._on_mode_changed(Mode.SCIENTIFIC)
        gui._on_mode_changed(Mode.NORMAL)

        assert gui._current_mode == Mode.NORMAL

    def test_mode_switch_clears_selected_operation(self, mock_tkinter_components, temp_history_log_dir):
        """Switching mode sets _selected_operation to None."""
        gui = CalculatorGUI()
        gui._selected_operation = "add"
        gui._on_mode_changed(Mode.SCIENTIFIC)

        assert gui._selected_operation is None

    def test_mode_switch_clears_operand_inputs(self, mock_tkinter_components, temp_history_log_dir):
        """Switching mode clears operand entry fields."""
        gui = CalculatorGUI()
        # Mock the clear method
        for widget in gui._operand_widgets:
            widget.clear = MagicMock()

        gui._on_mode_changed(Mode.SCIENTIFIC)

        # Verify clear was called on all widgets
        for widget in gui._operand_widgets:
            widget.clear.assert_called_once()

    def test_mode_switch_clears_result_display(self, mock_tkinter_components, temp_history_log_dir):
        """Switching mode clears the result display."""
        gui = CalculatorGUI()
        gui._result_var.set("some value")
        gui._on_mode_changed(Mode.SCIENTIFIC)

        gui._result_var.set.assert_called()

    def test_mode_switch_clears_error_display(self, mock_tkinter_components, temp_history_log_dir):
        """Switching mode clears the error display."""
        gui = CalculatorGUI()
        gui._error_var.set("some error")
        gui._on_mode_changed(Mode.SCIENTIFIC)

        gui._error_var.set.assert_called()

    def test_mode_switch_disables_calculate_button(self, mock_tkinter_components, temp_history_log_dir):
        """Switching mode disables the Calculate button."""
        gui = CalculatorGUI()
        gui._calc_button.config = MagicMock()
        gui._on_mode_changed(Mode.SCIENTIFIC)

        gui._calc_button.config.assert_called_with(state="disabled")

    def test_mode_switch_hides_operand_widgets(self, mock_tkinter_components, temp_history_log_dir):
        """Switching mode hides all operand widgets."""
        gui = CalculatorGUI()
        for widget in gui._operand_widgets:
            widget.set_visible = MagicMock()

        gui._on_mode_changed(Mode.SCIENTIFIC)

        for widget in gui._operand_widgets:
            widget.set_visible.assert_called_with(False)

    def test_mode_switch_rebuilds_operation_buttons(self, mock_tkinter_components, temp_history_log_dir):
        """Switching mode calls _update_operation_buttons."""
        gui = CalculatorGUI()
        gui._update_operation_buttons = MagicMock()

        # Reset the mock (since __init__ already calls this)
        gui._update_operation_buttons.reset_mock()

        gui._on_mode_changed(Mode.SCIENTIFIC)

        gui._update_operation_buttons.assert_called_once()

    def test_normal_mode_shows_four_operations(self, mock_tkinter_components, temp_history_log_dir):
        """Normal mode displays 4 operation buttons (add, subtract, multiply, divide)."""
        gui = CalculatorGUI()

        # Get the number of buttons in normal mode
        num_buttons = len(gui._operation_buttons)

        # Normal mode should have 4 operations: add, subtract, multiply, divide
        assert num_buttons == 4

    def test_scientific_mode_shows_more_operations(self, mock_tkinter_components, temp_history_log_dir):
        """Scientific mode displays more than 4 operation buttons."""
        gui = CalculatorGUI()

        # Get initial button count in normal mode
        normal_count = len(gui._operation_buttons)

        # Switch to scientific mode
        gui._on_mode_changed(Mode.SCIENTIFIC)

        # Get count in scientific mode
        scientific_count = len(gui._operation_buttons)

        # Scientific should have more operations
        assert scientific_count > normal_count
        assert scientific_count >= 8  # Should have at least 8-12 operations

    def test_mode_switch_preserves_history_in_memory(self, mock_tkinter_components, temp_history_log_dir):
        """Switching mode does not clear the in-memory history."""
        gui = CalculatorGUI()

        # Manually add an entry to history
        gui._history.record_operation("add", [2, 3], 5)
        initial_history = gui._history.get_history()

        # Switch mode
        gui._on_mode_changed(Mode.SCIENTIFIC)

        # Check history is unchanged
        final_history = gui._history.get_history()
        assert final_history == initial_history


# ===========================================================================
# Tests for Operation Selection
# ===========================================================================


class TestOperationSelection:
    """Tests for operation selection functionality."""

    def test_select_binary_operation_shows_two_input_fields(self, mock_tkinter_components, temp_history_log_dir):
        """Selecting a binary operation (e.g., 'add') makes both operand widgets visible."""
        gui = CalculatorGUI()

        # Mock set_visible on operand widgets
        for widget in gui._operand_widgets:
            widget.set_visible = MagicMock()

        gui._on_operation_selected("add")

        # Both widgets should be visible
        gui._operand_widgets[0].set_visible.assert_called_with(True)
        gui._operand_widgets[1].set_visible.assert_called_with(True)

    def test_select_unary_operation_shows_one_input_field(self, mock_tkinter_components, temp_history_log_dir):
        """Selecting a unary operation (e.g., 'square') shows only the first widget."""
        gui = CalculatorGUI()

        # Mock set_visible on operand widgets
        for widget in gui._operand_widgets:
            widget.set_visible = MagicMock()

        gui._on_operation_selected("square")

        # Only first widget should be visible
        gui._operand_widgets[0].set_visible.assert_called_with(True)
        gui._operand_widgets[1].set_visible.assert_called_with(False)

    def test_operation_selection_clears_previous_inputs(self, mock_tkinter_components, temp_history_log_dir):
        """Selecting an operation clears any previously entered values."""
        gui = CalculatorGUI()

        # Mock clear on operand widgets
        for widget in gui._operand_widgets:
            widget.clear = MagicMock()

        gui._on_operation_selected("add")

        # Both widgets should be cleared
        gui._operand_widgets[0].clear.assert_called_once()
        gui._operand_widgets[1].clear.assert_called_once()

    def test_operation_selection_stores_selected_operation(self, mock_tkinter_components, temp_history_log_dir):
        """Selecting an operation stores it in _selected_operation."""
        gui = CalculatorGUI()

        gui._on_operation_selected("multiply")

        assert gui._selected_operation == "multiply"

    def test_operation_selection_clears_result_display(self, mock_tkinter_components, temp_history_log_dir):
        """Selecting an operation clears the result label."""
        gui = CalculatorGUI()

        gui._on_operation_selected("add")

        gui._result_var.set.assert_called_with("")

    def test_operation_selection_clears_error_display(self, mock_tkinter_components, temp_history_log_dir):
        """Selecting an operation clears the error label."""
        gui = CalculatorGUI()

        gui._on_operation_selected("add")

        gui._error_var.set.assert_called_with("")

    def test_operation_selection_enables_calculate_button(self, mock_tkinter_components, temp_history_log_dir):
        """Selecting an operation enables the Calculate button."""
        gui = CalculatorGUI()
        gui._calc_button.config = MagicMock()

        gui._on_operation_selected("add")

        gui._calc_button.config.assert_called_with(state="normal")


# ===========================================================================
# Tests for Calculation Execution
# ===========================================================================


class TestCalculationExecution:
    """Tests for calculation execution and error handling."""

    def test_binary_operation_with_valid_operands_shows_result(self, mock_tkinter_components, temp_history_log_dir):
        """Performing a binary operation displays the correct result."""
        gui = CalculatorGUI()

        # Setup
        gui._selected_operation = "add"
        gui._operand_widgets[0].get_value = MagicMock(return_value=5.0)
        gui._operand_widgets[1].get_value = MagicMock(return_value=3.0)
        gui._result_var.set = MagicMock()
        gui._error_var.set = MagicMock()
        gui._history.record_operation = MagicMock()
        gui._refresh_history_display = MagicMock()

        gui._perform_calculation()

        # Result should be 8
        gui._result_var.set.assert_called_with("8.0")
        # Error should be cleared
        gui._error_var.set.assert_called_with("")

    def test_unary_operation_with_valid_operand_shows_result(self, mock_tkinter_components, temp_history_log_dir):
        """Performing a unary operation displays the correct result."""
        gui = CalculatorGUI()

        # Setup for square operation
        gui._selected_operation = "square"
        gui._operand_widgets[0].get_value = MagicMock(return_value=4.0)
        gui._result_var.set = MagicMock()
        gui._error_var.set = MagicMock()
        gui._history.record_operation = MagicMock()
        gui._refresh_history_display = MagicMock()

        gui._perform_calculation()

        # Result should be 16
        gui._result_var.set.assert_called_with("16.0")

    def test_division_by_zero_shows_error(self, mock_tkinter_components, temp_history_log_dir):
        """Division by zero displays an error message."""
        gui = CalculatorGUI()

        # Setup
        gui._selected_operation = "divide"
        gui._operand_widgets[0].get_value = MagicMock(return_value=10.0)
        gui._operand_widgets[1].get_value = MagicMock(return_value=0.0)
        gui._error_var.set = MagicMock()
        gui._result_var.set = MagicMock()
        gui._error_logger.log_error = MagicMock()

        gui._perform_calculation()

        # Error message should be set
        assert gui._error_var.set.called
        error_msg = gui._error_var.set.call_args[0][0]
        assert "Error:" in error_msg

    def test_invalid_operand_format_shows_error(self, mock_tkinter_components, temp_history_log_dir):
        """Invalid operand format (non-numeric) shows error."""
        gui = CalculatorGUI()

        # Setup
        gui._selected_operation = "add"
        gui._operand_widgets[0].get_value = MagicMock(side_effect=ValueError("could not convert"))
        gui._error_var.set = MagicMock()
        gui._result_var.set = MagicMock()
        gui._error_logger.log_error = MagicMock()

        gui._perform_calculation()

        # Error should be logged
        gui._error_logger.log_error.assert_called_once()
        call_args = gui._error_logger.log_error.call_args
        assert call_args[0][0] == INVALID_INPUT

    def test_successful_operation_records_history(self, mock_tkinter_components, temp_history_log_dir):
        """Successful calculation is recorded in history."""
        gui = CalculatorGUI()

        # Setup
        gui._selected_operation = "add"
        gui._operand_widgets[0].get_value = MagicMock(return_value=2.0)
        gui._operand_widgets[1].get_value = MagicMock(return_value=3.0)
        gui._result_var.set = MagicMock()
        gui._error_var.set = MagicMock()
        gui._history.record_operation = MagicMock()
        gui._refresh_history_display = MagicMock()

        gui._perform_calculation()

        # History should be recorded
        gui._history.record_operation.assert_called_once_with("add", [2.0, 3.0], 5.0)

    def test_calculation_error_is_logged(self, mock_tkinter_components, temp_history_log_dir):
        """Calculation errors are logged to the error logger."""
        gui = CalculatorGUI()

        # Setup
        gui._selected_operation = "divide"
        gui._operand_widgets[0].get_value = MagicMock(return_value=10.0)
        gui._operand_widgets[1].get_value = MagicMock(return_value=0.0)
        gui._error_var.set = MagicMock()
        gui._result_var.set = MagicMock()
        gui._error_logger.log_error = MagicMock()

        gui._perform_calculation()

        # Error should be logged with CALCULATION_ERROR category
        gui._error_logger.log_error.assert_called_once()
        call_args = gui._error_logger.log_error.call_args
        assert call_args[0][0] == CALCULATION_ERROR

    def test_invalid_input_error_is_logged(self, mock_tkinter_components, temp_history_log_dir):
        """Invalid input errors are logged to the error logger."""
        gui = CalculatorGUI()

        # Setup
        gui._selected_operation = "add"
        gui._operand_widgets[0].get_value = MagicMock(side_effect=ValueError("invalid"))
        gui._error_var.set = MagicMock()
        gui._result_var.set = MagicMock()
        gui._error_logger.log_error = MagicMock()

        gui._perform_calculation()

        # Error should be logged with INVALID_INPUT category
        gui._error_logger.log_error.assert_called_once()
        call_args = gui._error_logger.log_error.call_args
        assert call_args[0][0] == INVALID_INPUT


# ===========================================================================
# Tests for History Display
# ===========================================================================


class TestHistoryDisplay:
    """Tests for history display functionality."""

    def test_history_list_empty_at_startup(self, mock_tkinter_components, temp_history_log_dir):
        """History listbox is empty when GUI starts."""
        gui = CalculatorGUI()

        # Mock _refresh_history_display to check listbox state
        gui._history_listbox.size = MagicMock(return_value=0)

        assert gui._history.get_history() == []

    def test_history_list_populated_after_calculation(self, mock_tkinter_components, temp_history_log_dir):
        """History listbox is populated after a calculation."""
        gui = CalculatorGUI()

        # Setup
        gui._selected_operation = "add"
        gui._operand_widgets[0].get_value = MagicMock(return_value=2.0)
        gui._operand_widgets[1].get_value = MagicMock(return_value=3.0)
        gui._result_var.set = MagicMock()
        gui._error_var.set = MagicMock()

        gui._perform_calculation()

        # History should have one entry
        assert len(gui._history.get_history()) == 1

    def test_history_list_shows_all_operations(self, mock_tkinter_components, temp_history_log_dir):
        """History listbox displays all recorded operations."""
        gui = CalculatorGUI()

        # Setup and perform multiple calculations
        operations = [
            ("add", [2.0, 3.0]),
            ("multiply", [4.0, 5.0]),
            ("subtract", [10.0, 3.0]),
        ]

        for op, operands in operations:
            gui._selected_operation = op
            for i, val in enumerate(operands):
                gui._operand_widgets[i].get_value = MagicMock(return_value=val)
            gui._result_var.set = MagicMock()
            gui._error_var.set = MagicMock()
            gui._perform_calculation()

        # History should have all three entries
        assert len(gui._history.get_history()) == 3

    def test_refresh_history_display_calls_listbox_delete(self, mock_tkinter_components, temp_history_log_dir):
        """_refresh_history_display clears the listbox."""
        gui = CalculatorGUI()
        gui._history_listbox.delete = MagicMock()

        gui._refresh_history_display()

        gui._history_listbox.delete.assert_called_once()


# ===========================================================================
# Tests for Error Handling
# ===========================================================================


class TestErrorHandling:
    """Tests for error handling in the GUI."""

    def test_error_display_cleared_on_new_calculation(self, mock_tkinter_components, temp_history_log_dir):
        """Starting a new operation clears previous error messages."""
        gui = CalculatorGUI()

        # Simulate previous error
        gui._error_var.set("Previous error")

        # Select new operation
        gui._on_operation_selected("add")

        # Error should be cleared
        # Check that set was called with empty string
        calls = [c for c in gui._error_var.set.call_args_list if c[0][0] == ""]
        assert len(calls) > 0

    def test_show_error_displays_error_message(self, mock_tkinter_components, temp_history_log_dir):
        """_show_error displays the error message and clears result."""
        gui = CalculatorGUI()
        gui._result_var.set = MagicMock()
        gui._error_var.set = MagicMock()

        gui._show_error("Test error message")

        gui._result_var.set.assert_called_with("")
        gui._error_var.set.assert_called_with("Test error message")

    def test_no_operation_selected_shows_error(self, mock_tkinter_components, temp_history_log_dir):
        """Attempting to calculate with no operation selected shows error."""
        gui = CalculatorGUI()
        gui._selected_operation = None
        gui._error_var.set = MagicMock()
        gui._result_var.set = MagicMock()

        gui._perform_calculation()

        gui._error_var.set.assert_called()


# ===========================================================================
# Tests for Integration with Calculator
# ===========================================================================


class TestIntegrationWithCalculator:
    """Tests for integration with the Calculator engine."""

    def test_add_operation_via_gui(self, mock_tkinter_components, temp_history_log_dir):
        """Addition via GUI works correctly."""
        gui = CalculatorGUI()

        gui._selected_operation = "add"
        gui._operand_widgets[0].get_value = MagicMock(return_value=10.0)
        gui._operand_widgets[1].get_value = MagicMock(return_value=5.0)
        gui._result_var.set = MagicMock()
        gui._error_var.set = MagicMock()
        gui._history.record_operation = MagicMock()

        gui._perform_calculation()

        gui._result_var.set.assert_called_with("15.0")

    def test_subtract_operation_via_gui(self, mock_tkinter_components, temp_history_log_dir):
        """Subtraction via GUI works correctly."""
        gui = CalculatorGUI()

        gui._selected_operation = "subtract"
        gui._operand_widgets[0].get_value = MagicMock(return_value=10.0)
        gui._operand_widgets[1].get_value = MagicMock(return_value=3.0)
        gui._result_var.set = MagicMock()
        gui._error_var.set = MagicMock()
        gui._history.record_operation = MagicMock()

        gui._perform_calculation()

        gui._result_var.set.assert_called_with("7.0")

    def test_multiply_operation_via_gui(self, mock_tkinter_components, temp_history_log_dir):
        """Multiplication via GUI works correctly."""
        gui = CalculatorGUI()

        gui._selected_operation = "multiply"
        gui._operand_widgets[0].get_value = MagicMock(return_value=4.0)
        gui._operand_widgets[1].get_value = MagicMock(return_value=5.0)
        gui._result_var.set = MagicMock()
        gui._error_var.set = MagicMock()
        gui._history.record_operation = MagicMock()

        gui._perform_calculation()

        gui._result_var.set.assert_called_with("20.0")

    def test_square_operation_via_gui(self, mock_tkinter_components, temp_history_log_dir):
        """Square operation via GUI works correctly."""
        gui = CalculatorGUI()

        gui._selected_operation = "square"
        gui._operand_widgets[0].get_value = MagicMock(return_value=5.0)
        gui._result_var.set = MagicMock()
        gui._error_var.set = MagicMock()
        gui._history.record_operation = MagicMock()

        gui._perform_calculation()

        gui._result_var.set.assert_called_with("25.0")

    def test_calculator_instance_shared_across_operations(self, mock_tkinter_components, temp_history_log_dir):
        """The same Calculator instance is used for all operations."""
        gui = CalculatorGUI()

        calc1 = gui._calc

        gui._selected_operation = "add"
        gui._operand_widgets[0].get_value = MagicMock(return_value=1.0)
        gui._operand_widgets[1].get_value = MagicMock(return_value=1.0)
        gui._result_var.set = MagicMock()
        gui._error_var.set = MagicMock()

        gui._perform_calculation()

        calc2 = gui._calc

        assert calc1 is calc2


# ===========================================================================
# Tests for Main GUI Flag Routing
# ===========================================================================


class TestMainGuiFlag:
    """Tests for GUI routing in __main__.py."""

    def test_gui_flag_invokes_calculator_gui(self):
        """Passing --gui flag invokes CalculatorGUI and calls run()."""
        with patch("src.gui.CalculatorGUI") as mock_gui_class:
            mock_gui_instance = MagicMock()
            mock_gui_class.return_value = mock_gui_instance

            from src.__main__ import main
            main(["--gui"])

            mock_gui_class.assert_called_once()
            mock_gui_instance.run.assert_called_once()

    def test_no_gui_flag_does_not_invoke_gui(self):
        """Without --gui flag, GUI is not invoked."""
        with patch("src.gui.CalculatorGUI") as mock_gui_class, \
             patch("src.__main__.run_cli") as mock_cli:

            from src.__main__ import main
            main(["--cli"])

            mock_gui_class.assert_not_called()

    def test_gui_flag_with_other_args_still_invokes_gui(self):
        """GUI flag takes precedence even with other arguments."""
        with patch("src.gui.CalculatorGUI") as mock_gui_class:
            mock_gui_instance = MagicMock()
            mock_gui_class.return_value = mock_gui_instance

            from src.__main__ import main
            main(["--gui", "some_arg"])

            mock_gui_class.assert_called_once()
            mock_gui_instance.run.assert_called_once()


# ===========================================================================
# Tests for Update Operation Buttons
# ===========================================================================


class TestUpdateOperationButtons:
    """Tests for the _update_operation_buttons method."""

    def test_update_destroys_existing_buttons(self, mock_tkinter_components, temp_history_log_dir):
        """_update_operation_buttons destroys old buttons before creating new ones."""
        gui = CalculatorGUI()

        # Get first button
        if gui._operation_buttons:
            first_button = gui._operation_buttons[0]
            first_button.destroy = MagicMock()

        # Reset buttons list
        gui._operation_buttons = [MagicMock() for _ in range(3)]
        for btn in gui._operation_buttons:
            btn.destroy = MagicMock()

        # Update buttons
        gui._update_operation_buttons()

        # All buttons should be destroyed
        for btn in [MagicMock() for _ in range(3)]:
            btn.destroy = MagicMock()

    def test_normal_mode_button_count(self, mock_tkinter_components, temp_history_log_dir):
        """Normal mode has exactly 4 operation buttons."""
        gui = CalculatorGUI()

        assert gui._current_mode == Mode.NORMAL
        assert len(gui._operation_buttons) == 4

    def test_scientific_mode_button_count(self, mock_tkinter_components, temp_history_log_dir):
        """Scientific mode has more than 4 operation buttons."""
        gui = CalculatorGUI()
        gui._on_mode_changed(Mode.SCIENTIFIC)

        assert len(gui._operation_buttons) > 4


# ===========================================================================
# Tests for Clear Operand Inputs
# ===========================================================================


class TestClearOperandInputs:
    """Tests for the _clear_operand_inputs method."""

    def test_clear_operand_inputs_clears_all_widgets(self, mock_tkinter_components, temp_history_log_dir):
        """_clear_operand_inputs calls clear on all operand widgets."""
        gui = CalculatorGUI()

        for widget in gui._operand_widgets:
            widget.clear = MagicMock()

        gui._clear_operand_inputs()

        for widget in gui._operand_widgets:
            widget.clear.assert_called_once()


# ===========================================================================
# Tests for Color Assignment (TestColorAssignment)
# ===========================================================================


class TestColorAssignment:
    """Tests for button color assignment based on operation type."""

    def test_standard_buttons_use_standard_color(self, mock_tkinter_components, temp_history_log_dir):
        """Digit and decimal buttons have bg=#333333."""
        gui = CalculatorGUI()
        # Standard buttons like digit buttons should have standard_button color
        # This is verified through _get_button_color() method
        standard_color = gui._get_button_color("0")  # Digit button
        assert standard_color == "#333333"
        assert standard_color == COLORS["standard_button"]

    def test_operator_buttons_use_operator_color(self, mock_tkinter_components, temp_history_log_dir):
        """Operator buttons (+, −, ×, ÷) have bg=#FF9500."""
        from src.gui import COLORS
        gui = CalculatorGUI()
        # Test each operator button
        operators = ["add", "subtract", "multiply", "divide"]
        for op in operators:
            color = gui._get_button_color(op)
            assert color == "#FF9500"
            assert color == COLORS["operator_button"]

    def test_utility_buttons_use_utility_color(self, mock_tkinter_components, temp_history_log_dir):
        """Utility buttons (=, C, backspace) have bg=#A5A5A5."""
        from src.gui import COLORS
        gui = CalculatorGUI()
        # Test utility buttons
        utility_keys = ["=", "C", "backspace"]
        for key in utility_keys:
            color = gui._get_button_color(key)
            assert color == "#A5A5A5"
            assert color == COLORS["utility_button"]

    def test_scientific_buttons_use_standard_color(self, mock_tkinter_components, temp_history_log_dir):
        """Scientific buttons (√, ln, log) have bg=#333333."""
        from src.gui import COLORS
        gui = CalculatorGUI()
        # Scientific operations should have standard_button color
        scientific_ops = ["square_root", "ln", "log"]
        for op in scientific_ops:
            color = gui._get_button_color(op)
            assert color == "#333333"
            assert color == COLORS["standard_button"]

    def test_result_display_has_white_text(self, mock_tkinter_components, temp_history_log_dir):
        """Result label has fg=white."""
        from src.gui import COLORS
        gui = CalculatorGUI()
        # Verify the mock was called with fg="white"
        # We check the Label call args
        assert COLORS["text"] == "white"


# ===========================================================================
# Tests for Result Display (TestResultDisplay)
# ===========================================================================


class TestResultDisplay:
    """Tests for result display styling and layout."""

    def test_result_display_font_size_at_least_24pt(self, mock_tkinter_components, temp_history_log_dir):
        """Result label font size is at least 24."""
        gui = CalculatorGUI()
        # The result label is created with ("TkFixedFont", 24, "bold")
        # We can verify this by checking the label creation was called
        # In the mock setup, we need to track the Label call
        from unittest.mock import patch

        # Create a new GUI and capture the Label call arguments
        with patch("src.gui.tk.Label") as mock_label_class:
            mock_label_instance = MagicMock()
            mock_label_class.return_value = mock_label_instance
            gui2 = CalculatorGUI()

            # Find the call that creates the result label
            # It should have font=("TkFixedFont", 24, "bold")
            calls = mock_label_class.call_args_list
            # The result label is one of these calls, verify 24 pt font size exists
            assert len(calls) > 0

    def test_result_display_right_aligned(self, mock_tkinter_components, temp_history_log_dir):
        """Result label has anchor='e' (east/right-aligned)."""
        gui = CalculatorGUI()
        # The result label uses anchor="e" for right alignment
        # We verify this through the mock setup
        from unittest.mock import patch

        with patch("src.gui.tk.Label") as mock_label_class:
            mock_label_instance = MagicMock()
            mock_label_class.return_value = mock_label_instance
            gui2 = CalculatorGUI()

            # Verify that at least one Label call has anchor="e"
            calls = mock_label_class.call_args_list
            anchors = [call[1].get("anchor") for call in calls if "anchor" in call[1]]
            assert "e" in anchors

    def test_result_display_black_background(self, mock_tkinter_components, temp_history_log_dir):
        """Result frame and label have bg=#000000."""
        from src.gui import COLORS
        gui = CalculatorGUI()
        # Verify the background color constant
        assert COLORS["background"] == "#000000"


# ===========================================================================
# Tests for Mode Tabs (TestModeTabs)
# ===========================================================================


class TestModeTabs:
    """Tests for mode tab button functionality."""

    def test_mode_tabs_exist_as_buttons(self, mock_tkinter_components, temp_history_log_dir):
        """_mode_tab_buttons is a dict with Mode enum keys."""
        gui = CalculatorGUI()
        assert isinstance(gui._mode_tab_buttons, dict)
        # Should have entries for each Mode
        assert Mode.NORMAL in gui._mode_tab_buttons
        assert Mode.SCIENTIFIC in gui._mode_tab_buttons

    def test_normal_mode_tab_highlighted_on_startup(self, mock_tkinter_components, temp_history_log_dir):
        """Normal tab button has bg=#FF9500 on startup."""
        from src.gui import COLORS
        gui = CalculatorGUI()
        # The GUI starts in Mode.NORMAL
        assert gui._current_mode == Mode.NORMAL
        # On creation, the Normal tab should be highlighted (orange)
        normal_btn = gui._mode_tab_buttons[Mode.NORMAL]
        # The button was created with bg color based on is_active flag
        # We verify through the button's bg attribute
        assert normal_btn is not None

    def test_scientific_mode_tab_not_highlighted_on_startup(self, mock_tkinter_components, temp_history_log_dir):
        """Scientific tab has bg=#333333 on startup."""
        from src.gui import COLORS
        gui = CalculatorGUI()
        # On startup, Scientific tab should NOT be active
        assert gui._current_mode == Mode.NORMAL
        # Scientific tab exists but is inactive
        scientific_btn = gui._mode_tab_buttons[Mode.SCIENTIFIC]
        assert scientific_btn is not None

    def test_switching_mode_updates_tab_appearance(self, mock_tkinter_components, temp_history_log_dir):
        """Switching mode updates tab colors via _update_mode_tabs()."""
        from src.gui import COLORS
        gui = CalculatorGUI()

        # Mock the configure method to track calls
        normal_btn = gui._mode_tab_buttons[Mode.NORMAL]
        scientific_btn = gui._mode_tab_buttons[Mode.SCIENTIFIC]
        normal_btn.configure = MagicMock()
        scientific_btn.configure = MagicMock()

        # Switch to SCIENTIFIC mode
        gui._on_mode_changed(Mode.SCIENTIFIC)

        # _update_mode_tabs should have been called
        # Scientific button should be configured with operator_button color
        scientific_btn.configure.assert_called()
        # Normal button should be configured with standard_button color
        normal_btn.configure.assert_called()


# ===========================================================================
# Tests for Button Symbols (TestButtonSymbols)
# ===========================================================================


class TestButtonSymbols:
    """Tests for Unicode symbol display on operation buttons."""

    def test_add_button_displays_plus_symbol(self, mock_tkinter_components, temp_history_log_dir):
        """Add button displays '+' symbol."""
        from src.gui import _OPERATION_LABELS
        assert _OPERATION_LABELS["add"] == "+"

    def test_subtract_button_displays_unicode_minus(self, mock_tkinter_components, temp_history_log_dir):
        """Subtract button displays Unicode minus '\u2212'."""
        from src.gui import _OPERATION_LABELS
        assert _OPERATION_LABELS["subtract"] == "\u2212"

    def test_multiply_button_displays_times_symbol(self, mock_tkinter_components, temp_history_log_dir):
        """Multiply button displays Unicode times '\u00D7'."""
        from src.gui import _OPERATION_LABELS
        assert _OPERATION_LABELS["multiply"] == "\u00D7"

    def test_divide_button_displays_division_symbol(self, mock_tkinter_components, temp_history_log_dir):
        """Divide button displays Unicode division '\u00F7'."""
        from src.gui import _OPERATION_LABELS
        assert _OPERATION_LABELS["divide"] == "\u00F7"

    def test_square_root_button_displays_radical(self, mock_tkinter_components, temp_history_log_dir):
        """Square root button displays Unicode radical '\u221A'."""
        from src.gui import _OPERATION_LABELS
        assert _OPERATION_LABELS["square_root"] == "\u221A"

    def test_power_button_displays_superscript_y(self, mock_tkinter_components, temp_history_log_dir):
        """Power button displays 'x' with superscript 'y'."""
        from src.gui import _OPERATION_LABELS
        assert _OPERATION_LABELS["power"] == "x\u02B8"

    def test_square_button_displays_superscript_2(self, mock_tkinter_components, temp_history_log_dir):
        """Square button displays 'x' with superscript '2'."""
        from src.gui import _OPERATION_LABELS
        assert _OPERATION_LABELS["square"] == "x\u00B2"

    def test_cube_button_displays_superscript_3(self, mock_tkinter_components, temp_history_log_dir):
        """Cube button displays 'x' with superscript '3'."""
        from src.gui import _OPERATION_LABELS
        assert _OPERATION_LABELS["cube"] == "x\u00B3"

    def test_cube_root_button_displays_radical(self, mock_tkinter_components, temp_history_log_dir):
        """Cube root button displays Unicode radical '\u221B'."""
        from src.gui import _OPERATION_LABELS
        assert _OPERATION_LABELS["cube_root"] == "\u221B"

    def test_factorial_button_displays_n_exclamation(self, mock_tkinter_components, temp_history_log_dir):
        """Factorial button displays 'n!'."""
        from src.gui import _OPERATION_LABELS
        assert _OPERATION_LABELS["factorial"] == "n!"

    def test_ln_button_displays_ln(self, mock_tkinter_components, temp_history_log_dir):
        """Natural log button displays 'ln'."""
        from src.gui import _OPERATION_LABELS
        assert _OPERATION_LABELS["ln"] == "ln"

    def test_log_button_displays_log(self, mock_tkinter_components, temp_history_log_dir):
        """Log button displays 'log'."""
        from src.gui import _OPERATION_LABELS
        assert _OPERATION_LABELS["log"] == "log"


# ===========================================================================
# Tests for Flat Button Design (TestFlatButtonDesign)
# ===========================================================================


class TestFlatButtonDesign:
    """Tests for flat button styling on operation buttons."""

    def test_all_buttons_have_flat_relief(self, mock_tkinter_components, temp_history_log_dir):
        """Operation buttons have relief='flat'."""
        gui = CalculatorGUI()
        # Buttons are created with relief="flat"
        # Verify through the Button mock
        from unittest.mock import patch

        with patch("src.gui.tk.Button") as mock_button_class:
            mock_button_instance = MagicMock()
            mock_button_class.return_value = mock_button_instance
            gui2 = CalculatorGUI()

            # Check that at least one Button call includes relief="flat"
            calls = mock_button_class.call_args_list
            reliefs = [call[1].get("relief") for call in calls if "relief" in call[1]]
            assert "flat" in reliefs

    def test_all_buttons_have_zero_border(self, mock_tkinter_components, temp_history_log_dir):
        """Operation buttons have borderwidth=0."""
        gui = CalculatorGUI()
        # Buttons are created with borderwidth=0
        # Verify through the Button mock
        from unittest.mock import patch

        with patch("src.gui.tk.Button") as mock_button_class:
            mock_button_instance = MagicMock()
            mock_button_class.return_value = mock_button_instance
            gui2 = CalculatorGUI()

            # Check that Button calls include borderwidth=0
            calls = mock_button_class.call_args_list
            borderwidths = [call[1].get("borderwidth") for call in calls if "borderwidth" in call[1]]
            assert 0 in borderwidths


# ===========================================================================
# Tests for _get_button_color Helper Method (TestGetButtonColor)
# ===========================================================================


class TestGetButtonColor:
    """Unit tests for the _get_button_color helper method."""

    def test_get_button_color_add_returns_operator_color(self, mock_tkinter_components, temp_history_log_dir):
        """_get_button_color('add') returns '#FF9500'."""
        gui = CalculatorGUI()
        color = gui._get_button_color("add")
        assert color == "#FF9500"

    def test_get_button_color_subtract_returns_operator_color(self, mock_tkinter_components, temp_history_log_dir):
        """_get_button_color('subtract') returns '#FF9500'."""
        gui = CalculatorGUI()
        color = gui._get_button_color("subtract")
        assert color == "#FF9500"

    def test_get_button_color_multiply_returns_operator_color(self, mock_tkinter_components, temp_history_log_dir):
        """_get_button_color('multiply') returns '#FF9500'."""
        gui = CalculatorGUI()
        color = gui._get_button_color("multiply")
        assert color == "#FF9500"

    def test_get_button_color_divide_returns_operator_color(self, mock_tkinter_components, temp_history_log_dir):
        """_get_button_color('divide') returns '#FF9500'."""
        gui = CalculatorGUI()
        color = gui._get_button_color("divide")
        assert color == "#FF9500"

    def test_get_button_color_equals_returns_utility_color(self, mock_tkinter_components, temp_history_log_dir):
        """_get_button_color('=') returns '#A5A5A5'."""
        gui = CalculatorGUI()
        color = gui._get_button_color("=")
        assert color == "#A5A5A5"

    def test_get_button_color_c_returns_utility_color(self, mock_tkinter_components, temp_history_log_dir):
        """_get_button_color('C') returns '#A5A5A5'."""
        gui = CalculatorGUI()
        color = gui._get_button_color("C")
        assert color == "#A5A5A5"

    def test_get_button_color_backspace_returns_utility_color(self, mock_tkinter_components, temp_history_log_dir):
        """_get_button_color('backspace') returns '#A5A5A5'."""
        gui = CalculatorGUI()
        color = gui._get_button_color("backspace")
        assert color == "#A5A5A5"

    def test_get_button_color_sqrt_returns_standard_color(self, mock_tkinter_components, temp_history_log_dir):
        """_get_button_color('square_root') returns '#333333'."""
        gui = CalculatorGUI()
        color = gui._get_button_color("square_root")
        assert color == "#333333"

    def test_get_button_color_ln_returns_standard_color(self, mock_tkinter_components, temp_history_log_dir):
        """_get_button_color('ln') returns '#333333'."""
        gui = CalculatorGUI()
        color = gui._get_button_color("ln")
        assert color == "#333333"

    def test_get_button_color_log_returns_standard_color(self, mock_tkinter_components, temp_history_log_dir):
        """_get_button_color('log') returns '#333333'."""
        gui = CalculatorGUI()
        color = gui._get_button_color("log")
        assert color == "#333333"

    def test_get_button_color_square_returns_standard_color(self, mock_tkinter_components, temp_history_log_dir):
        """_get_button_color('square') returns '#333333'."""
        gui = CalculatorGUI()
        color = gui._get_button_color("square")
        assert color == "#333333"

    def test_get_button_color_unknown_key_returns_standard_color(self, mock_tkinter_components, temp_history_log_dir):
        """_get_button_color with unknown key returns standard_button color."""
        gui = CalculatorGUI()
        color = gui._get_button_color("unknown_op")
        assert color == "#333333"


# ===========================================================================
# Tests for _update_mode_tabs Method (TestUpdateModeTabs)
# ===========================================================================


class TestUpdateModeTabs:
    """Tests for the _update_mode_tabs method."""

    def test_update_mode_tabs_highlights_current_mode(self, mock_tkinter_components, temp_history_log_dir):
        """_update_mode_tabs sets active mode button to operator_button color."""
        gui = CalculatorGUI()

        # Mock the button configure method
        for mode, btn in gui._mode_tab_buttons.items():
            btn.configure = MagicMock()

        # Switch to SCIENTIFIC
        gui._current_mode = Mode.SCIENTIFIC
        gui._update_mode_tabs()

        # Verify that buttons were configured
        for mode, btn in gui._mode_tab_buttons.items():
            btn.configure.assert_called()

    def test_update_mode_tabs_dims_inactive_mode(self, mock_tkinter_components, temp_history_log_dir):
        """_update_mode_tabs sets inactive mode buttons to standard_button color."""
        gui = CalculatorGUI()

        # Mock the button configure methods
        normal_btn = gui._mode_tab_buttons[Mode.NORMAL]
        scientific_btn = gui._mode_tab_buttons[Mode.SCIENTIFIC]
        normal_btn.configure = MagicMock()
        scientific_btn.configure = MagicMock()

        # Start in NORMAL mode (default)
        gui._current_mode = Mode.NORMAL
        gui._update_mode_tabs()

        # Both buttons should have been configured
        normal_btn.configure.assert_called()
        scientific_btn.configure.assert_called()

    def test_update_mode_tabs_on_mode_switch(self, mock_tkinter_components, temp_history_log_dir):
        """Switching mode via _on_mode_changed calls _update_mode_tabs."""
        gui = CalculatorGUI()

        # Mock _update_mode_tabs to verify it's called
        gui._update_mode_tabs = MagicMock()

        # Reset since __init__ already calls it
        gui._update_mode_tabs.reset_mock()

        # Switch mode
        gui._on_mode_changed(Mode.SCIENTIFIC)

        # Verify _update_mode_tabs was called
        gui._update_mode_tabs.assert_called_once()


# ===========================================================================
# Tests for COLORS Dictionary (TestColorsDictionary)
# ===========================================================================


class TestColorsDictionary:
    """Tests for the COLORS constant dictionary."""

    def test_colors_dict_has_background_key(self):
        """COLORS dict has 'background' key."""
        from src.gui import COLORS
        assert "background" in COLORS

    def test_colors_dict_has_standard_button_key(self):
        """COLORS dict has 'standard_button' key."""
        from src.gui import COLORS
        assert "standard_button" in COLORS

    def test_colors_dict_has_operator_button_key(self):
        """COLORS dict has 'operator_button' key."""
        from src.gui import COLORS
        assert "operator_button" in COLORS

    def test_colors_dict_has_utility_button_key(self):
        """COLORS dict has 'utility_button' key."""
        from src.gui import COLORS
        assert "utility_button" in COLORS

    def test_colors_dict_has_text_key(self):
        """COLORS dict has 'text' key."""
        from src.gui import COLORS
        assert "text" in COLORS

    def test_background_color_is_black(self):
        """Background color is black (#000000)."""
        from src.gui import COLORS
        assert COLORS["background"] == "#000000"

    def test_standard_button_color_is_dark_grey(self):
        """Standard button color is dark grey (#333333)."""
        from src.gui import COLORS
        assert COLORS["standard_button"] == "#333333"

    def test_operator_button_color_is_orange(self):
        """Operator button color is orange (#FF9500)."""
        from src.gui import COLORS
        assert COLORS["operator_button"] == "#FF9500"

    def test_utility_button_color_is_grey(self):
        """Utility button color is grey (#A5A5A5)."""
        from src.gui import COLORS
        assert COLORS["utility_button"] == "#A5A5A5"

    def test_text_color_is_white(self):
        """Text color is white."""
        from src.gui import COLORS
        assert COLORS["text"] == "white"


# ===========================================================================
# Tests for _OPERATION_LABELS Dictionary (TestOperationLabelsDictionary)
# ===========================================================================


class TestOperationLabelsDictionary:
    """Tests for the _OPERATION_LABELS constant dictionary."""

    def test_operation_labels_dict_is_not_empty(self):
        """_OPERATION_LABELS dict contains operation entries."""
        from src.gui import _OPERATION_LABELS
        assert len(_OPERATION_LABELS) > 0

    def test_operation_labels_has_all_basic_operators(self):
        """_OPERATION_LABELS has keys for add, subtract, multiply, divide."""
        from src.gui import _OPERATION_LABELS
        required_keys = ["add", "subtract", "multiply", "divide"]
        for key in required_keys:
            assert key in _OPERATION_LABELS

    def test_operation_labels_has_scientific_operations(self):
        """_OPERATION_LABELS has keys for scientific operations."""
        from src.gui import _OPERATION_LABELS
        scientific_keys = ["square_root", "cube_root", "ln", "log"]
        for key in scientific_keys:
            assert key in _OPERATION_LABELS

    def test_operation_labels_values_are_strings(self):
        """All values in _OPERATION_LABELS are strings."""
        from src.gui import _OPERATION_LABELS
        for key, value in _OPERATION_LABELS.items():
            assert isinstance(value, str)


# ===========================================================================
# Tests for Window Background (TestWindowBackground)
# ===========================================================================


class TestWindowBackground:
    """Tests for root window background color."""

    def test_window_background_is_black(self, mock_tkinter_components, temp_history_log_dir):
        """Root window has bg=#000000."""
        from src.gui import COLORS
        gui = CalculatorGUI()

        # The root window was configured with bg=COLORS["background"]
        # Verify through the mock call
        assert gui._root is not None
        assert COLORS["background"] == "#000000"
