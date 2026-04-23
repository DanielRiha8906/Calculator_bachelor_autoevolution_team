"""Integration tests for CalculatorGUI.

These tests run in a headless environment without a display server.
Tests use tk.Tk() with withdraw() to avoid window rendering, and mock
operations to prevent mainloop() from being called.
"""

from unittest import mock

import pytest

pytestmark = pytest.mark.gui

# Skip all tests in this module if tkinter is unavailable
tk = pytest.importorskip("tkinter")

from src.gui import CalculatorGUI
from src.session_history import SessionHistory
from src.validation import OperandValidationError


class TestCalculatorGUIInitialization:
    """Test suite for CalculatorGUI initialization."""

    @pytest.fixture
    def gui_setup(self):
        """Create a test GUI with withdrawn window."""
        root = tk.Tk()
        root.withdraw()
        history = SessionHistory()
        gui = CalculatorGUI(root, history)
        yield gui
        root.destroy()

    def test_gui_window_created(self, gui_setup):
        """Verify that the Tk root window is created and configured."""
        gui = gui_setup
        assert isinstance(gui.root, tk.Tk)
        assert gui.root.title() == "Calculator"

    def test_gui_widgets_exist(self, gui_setup):
        """Verify that key widget attributes are present."""
        gui = gui_setup
        assert hasattr(gui, "_mode_label")
        assert hasattr(gui, "_mode_button")
        assert hasattr(gui, "_ops_listbox")
        assert hasattr(gui, "_inputs_frame")
        assert hasattr(gui, "_execute_button")
        assert hasattr(gui, "_result_label")
        assert hasattr(gui, "_error_label")
        assert hasattr(gui, "_history_text")
        assert hasattr(gui, "_clear_history_button")

    def test_gui_initial_mode_is_normal(self, gui_setup):
        """Verify that the initial mode is Normal/Simple."""
        gui = gui_setup
        mode_label_text = gui._mode_label.cget("text")
        assert mode_label_text == "Normal"

    def test_gui_engine_components_initialized(self, gui_setup):
        """Verify that calculator engine components are created."""
        gui = gui_setup
        assert gui._calc is not None
        assert gui._registry is not None
        assert gui._mode_manager is not None

    def test_gui_history_initialized(self, gui_setup):
        """Verify that session history is properly set."""
        gui = gui_setup
        assert isinstance(gui._history, SessionHistory)
        assert gui._history.is_empty() is True


class TestCalculatorGUIOperations:
    """Test suite for CalculatorGUI operation execution."""

    @pytest.fixture
    def gui_setup(self):
        """Create a test GUI with withdrawn window."""
        root = tk.Tk()
        root.withdraw()
        history = SessionHistory()
        gui = CalculatorGUI(root, history)
        yield gui
        root.destroy()

    def test_two_operand_operation_add(self, gui_setup):
        """Verify addition with two operands executes and displays result."""
        gui = gui_setup
        # Select the "add" operation (first in normal mode)
        gui._ops_listbox.selection_set(0)
        # Call the handler directly since event_generate does not trigger callbacks in test context
        gui._on_operation_selected(None)

        # Verify operand fields were created
        assert len(gui._operand_entries) == 2

        # Set operands
        gui._operand_entries[0].insert(0, "5")
        gui._operand_entries[1].insert(0, "3")

        # Execute
        gui._execute_operation()

        # Verify result is displayed
        result_text = gui._result_label.cget("text")
        assert "8" in result_text or "8.0" in result_text

    def test_two_operand_operation_multiply(self, gui_setup):
        """Verify multiplication operation."""
        gui = gui_setup
        # Find and select the "multiply" operation
        for i in range(gui._ops_listbox.size()):
            item = gui._ops_listbox.get(i)
            if "multiply" in item.lower() or "multiplication" in item.lower():
                gui._ops_listbox.selection_set(i)
                gui._on_operation_selected(None)
                break

        if len(gui._operand_entries) == 2:
            gui._operand_entries[0].insert(0, "6")
            gui._operand_entries[1].insert(0, "7")
            gui._execute_operation()
            result_text = gui._result_label.cget("text")
            assert "42" in result_text

    def test_single_operand_operation_square(self, gui_setup):
        """Verify unary operation like square."""
        gui = gui_setup
        # Find and select the "square" operation
        for i in range(gui._ops_listbox.size()):
            item = gui._ops_listbox.get(i)
            if "square" in item.lower() and "root" not in item.lower():
                gui._ops_listbox.selection_set(i)
                gui._on_operation_selected(None)
                break

        if len(gui._operand_entries) == 1:
            gui._operand_entries[0].insert(0, "5")
            gui._execute_operation()
            result_text = gui._result_label.cget("text")
            assert "25" in result_text

    def test_division_by_zero_error(self, gui_setup):
        """Verify that division by zero displays error (not crash)."""
        gui = gui_setup
        # Select divide operation
        for i in range(gui._ops_listbox.size()):
            item = gui._ops_listbox.get(i)
            if "division" in item.lower():
                gui._ops_listbox.selection_set(i)
                gui._on_operation_selected(None)
                break

        if len(gui._operand_entries) == 2:
            gui._operand_entries[0].insert(0, "10")
            gui._operand_entries[1].insert(0, "0")
            gui._execute_operation()

            # Error should be displayed (not result)
            error_text = gui._error_label.cget("text")
            assert error_text != ""
            assert "Error" in error_text

    def test_invalid_operand_input_non_numeric(self, gui_setup):
        """Verify validation rejects non-numeric string."""
        gui = gui_setup
        # Select the "add" operation
        gui._ops_listbox.selection_set(0)
        gui._on_operation_selected(None)

        if len(gui._operand_entries) == 2:
            gui._operand_entries[0].insert(0, "abc")
            gui._operand_entries[1].insert(0, "5")
            gui._execute_operation()

            # Error should be displayed
            error_text = gui._error_label.cget("text")
            assert "Error" in error_text
            assert "not a valid number" in error_text

    def test_invalid_operand_input_empty_field(self, gui_setup):
        """Verify validation rejects empty operand fields."""
        gui = gui_setup
        # Select the "add" operation
        gui._ops_listbox.selection_set(0)
        gui._on_operation_selected(None)

        if len(gui._operand_entries) == 2:
            gui._operand_entries[0].insert(0, "5")
            # Leave second field empty
            gui._execute_operation()

            # Error should be displayed
            error_text = gui._error_label.cget("text")
            assert "Error" in error_text

    def test_execute_without_operation_selected(self, gui_setup):
        """Verify error when trying to execute without selecting an operation."""
        gui = gui_setup
        gui._execute_operation()

        error_text = gui._error_label.cget("text")
        assert "Error" in error_text
        assert "select" in error_text.lower()

    def test_factorial_with_integer(self, gui_setup):
        """Verify factorial operation with valid integer."""
        gui = gui_setup
        # Find and select the "factorial" operation
        for i in range(gui._ops_listbox.size()):
            item = gui._ops_listbox.get(i)
            if "factorial" in item.lower():
                gui._ops_listbox.selection_set(i)
                gui._on_operation_selected(None)
                break

        if len(gui._operand_entries) == 1:
            gui._operand_entries[0].insert(0, "5")
            gui._execute_operation()
            result_text = gui._result_label.cget("text")
            assert "120" in result_text

    def test_factorial_with_non_integer(self, gui_setup):
        """Verify factorial rejects non-integer input."""
        gui = gui_setup
        # Find and select the "factorial" operation
        for i in range(gui._ops_listbox.size()):
            item = gui._ops_listbox.get(i)
            if "factorial" in item.lower():
                gui._ops_listbox.selection_set(i)
                gui._on_operation_selected(None)
                break

        if len(gui._operand_entries) == 1:
            gui._operand_entries[0].insert(0, "5.5")
            gui._execute_operation()
            error_text = gui._error_label.cget("text")
            assert "Error" in error_text
            assert "integer" in error_text.lower()


class TestCalculatorGUIMode:
    """Test suite for CalculatorGUI mode switching."""

    @pytest.fixture
    def gui_setup(self):
        """Create a test GUI with withdrawn window."""
        root = tk.Tk()
        root.withdraw()
        history = SessionHistory()
        gui = CalculatorGUI(root, history)
        yield gui
        root.destroy()

    def test_mode_switch_changes_label(self, gui_setup):
        """Verify mode label changes after toggle."""
        gui = gui_setup
        initial_mode = gui._mode_label.cget("text")
        assert initial_mode == "Normal"

        gui._on_mode_switch()

        new_mode = gui._mode_label.cget("text")
        assert new_mode == "Scientific" or new_mode == "Sci"  # accommodate different display names

    def test_mode_switch_toggles_back(self, gui_setup):
        """Verify mode switch is bidirectional."""
        gui = gui_setup
        gui._on_mode_switch()
        gui._on_mode_switch()

        mode = gui._mode_label.cget("text")
        assert mode == "Normal"

    def test_scientific_operations_in_scientific_mode(self, gui_setup):
        """Verify scientific operations appear in Scientific mode."""
        gui = gui_setup
        # Collect operations in normal mode
        normal_ops = [gui._ops_listbox.get(i) for i in range(gui._ops_listbox.size())]

        # Switch to scientific
        gui._on_mode_switch()

        # Collect operations in scientific mode
        scientific_ops = [gui._ops_listbox.get(i) for i in range(gui._ops_listbox.size())]

        # Scientific mode should have more or same operations
        assert len(scientific_ops) >= len(normal_ops)

        # Check that scientific operations like sin, cos, tan are available
        scientific_names = " ".join(scientific_ops).lower()
        # At least one of sin/cos/tan should be present
        has_trig = "sin" in scientific_names or "cos" in scientific_names or "tan" in scientific_names
        assert has_trig

    def test_mode_switch_clears_result(self, gui_setup):
        """Verify that mode switch clears the result display."""
        gui = gui_setup
        gui._result_label.config(text="Previous result")

        gui._on_mode_switch()

        result = gui._result_label.cget("text")
        assert result == ""

    def test_mode_switch_clears_error(self, gui_setup):
        """Verify that mode switch clears any error message."""
        gui = gui_setup
        gui._error_label.config(text="Error: something")
        gui._error_label.grid()

        gui._on_mode_switch()

        error = gui._error_label.cget("text")
        assert error == ""


class TestCalculatorGUIHistory:
    """Test suite for CalculatorGUI history integration."""

    @pytest.fixture
    def gui_setup(self):
        """Create a test GUI with withdrawn window."""
        root = tk.Tk()
        root.withdraw()
        history = SessionHistory()
        gui = CalculatorGUI(root, history)
        yield gui
        root.destroy()

    def test_operation_recorded_in_history(self, gui_setup):
        """Verify that SessionHistory records op after execution."""
        gui = gui_setup
        # Select the "add" operation
        gui._ops_listbox.selection_set(0)
        gui._on_operation_selected(None)

        if len(gui._operand_entries) == 2:
            gui._operand_entries[0].insert(0, "5")
            gui._operand_entries[1].insert(0, "3")
            gui._execute_operation()

            # Verify history was updated
            assert not gui._history.is_empty()
            entries = gui._history.get_history()
            assert len(entries) == 1
            assert entries[0]["result"] == 8.0

    def test_multiple_operations_in_history(self, gui_setup):
        """Verify multiple operations are recorded in order."""
        gui = gui_setup
        # First operation: add
        gui._ops_listbox.selection_set(0)
        gui._on_operation_selected(None)
        gui._operand_entries[0].insert(0, "2")
        gui._operand_entries[1].insert(0, "3")
        gui._execute_operation()

        # Second operation: multiply (should be at index 2)
        for i in range(gui._ops_listbox.size()):
            if "multiply" in gui._ops_listbox.get(i).lower():
                # Clear previous selection before selecting new one
                gui._ops_listbox.selection_clear(0, tk.END)
                gui._ops_listbox.selection_set(i)
                gui._on_operation_selected(None)
                break

        # Clear previous entries
        for entry in gui._operand_entries:
            entry.delete(0, tk.END)

        gui._operand_entries[0].insert(0, "5")
        gui._operand_entries[1].insert(0, "4")
        gui._execute_operation()

        entries = gui._history.get_history()
        assert len(entries) == 2
        assert entries[0]["operation"] == "add"
        assert entries[1]["operation"] == "multiply"

    def test_clear_history_clears_session(self, gui_setup):
        """Verify that clear history button empties the session."""
        gui = gui_setup
        # Record an operation
        gui._ops_listbox.selection_set(0)
        gui._on_operation_selected(None)
        gui._operand_entries[0].insert(0, "5")
        gui._operand_entries[1].insert(0, "3")
        gui._execute_operation()

        assert not gui._history.is_empty()

        # Clear history
        gui._on_clear_history()

        assert gui._history.is_empty()

    def test_history_display_in_widget(self, gui_setup):
        """Verify history text widget displays operations."""
        gui = gui_setup
        # Record an operation
        gui._ops_listbox.selection_set(0)
        gui._on_operation_selected(None)
        gui._operand_entries[0].insert(0, "5")
        gui._operand_entries[1].insert(0, "3")
        gui._execute_operation()

        # Get text from history widget
        history_text = gui._history_text.get("1.0", tk.END).strip()
        assert "add" in history_text or "addition" in history_text.lower()
        assert "8" in history_text or "8.0" in history_text

    def test_history_text_widget_read_only(self, gui_setup):
        """Verify history text widget is read-only."""
        gui = gui_setup
        widget_state = gui._history_text.cget("state")
        assert widget_state == tk.DISABLED


class TestCalculatorGUIEdgeCases:
    """Test suite for edge cases and error handling."""

    @pytest.fixture
    def gui_setup(self):
        """Create a test GUI with withdrawn window."""
        root = tk.Tk()
        root.withdraw()
        history = SessionHistory()
        gui = CalculatorGUI(root, history)
        yield gui
        root.destroy()

    def test_operation_with_zero_operands(self, gui_setup):
        """Verify handling when no valid operands are provided."""
        gui = gui_setup
        gui._ops_listbox.selection_set(0)
        gui._on_operation_selected(None)

        # Don't set any operands, just execute
        gui._execute_operation()

        # Should show error
        error_text = gui._error_label.cget("text")
        assert "Error" in error_text

    def test_negative_operands(self, gui_setup):
        """Verify operations work with negative operands."""
        gui = gui_setup
        # Select subtract
        for i in range(gui._ops_listbox.size()):
            if "subtract" in gui._ops_listbox.get(i).lower():
                gui._ops_listbox.selection_set(i)
                gui._on_operation_selected(None)
                break

        if len(gui._operand_entries) == 2:
            gui._operand_entries[0].insert(0, "-5")
            gui._operand_entries[1].insert(0, "3")
            gui._execute_operation()

            result_text = gui._result_label.cget("text")
            assert "Error" not in result_text

    def test_very_large_operands(self, gui_setup):
        """Verify operations with very large numbers."""
        gui = gui_setup
        gui._ops_listbox.selection_set(0)
        gui._on_operation_selected(None)

        if len(gui._operand_entries) == 2:
            gui._operand_entries[0].insert(0, "1e100")
            gui._operand_entries[1].insert(0, "1e100")
            gui._execute_operation()

            # Should complete without crashing
            result_text = gui._result_label.cget("text")
            assert isinstance(result_text, str)

    def test_fractional_operands(self, gui_setup):
        """Verify operations with fractional operands."""
        gui = gui_setup
        gui._ops_listbox.selection_set(0)
        gui._on_operation_selected(None)

        if len(gui._operand_entries) == 2:
            gui._operand_entries[0].insert(0, "2.5")
            gui._operand_entries[1].insert(0, "1.5")
            gui._execute_operation()

            result_text = gui._result_label.cget("text")
            assert "4" in result_text or "4.0" in result_text
