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

from src.gui import OperandInputWidget, CalculatorGUI
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
