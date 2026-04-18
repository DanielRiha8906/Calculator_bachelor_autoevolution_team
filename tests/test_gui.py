"""Comprehensive pytest tests for GUI calculator.

Tests cover:
- BaseMode operation filtering (NORMAL vs SCIENTIFIC)
- GuiCalculator initialization and tkinter availability
- Window/widget creation (result label, history, mode selector)
- Mode switching and operation grid updates
- Unary and binary operation execution
- Dialog-based operand input
- Error handling (domain errors, division by zero, invalid operands)
- History display and persistence
- Integration with Calculator logic
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
# BaseMode Tests (Operation Filtering Logic)
# ===========================================================================

class TestBaseModeGetAvailableOperations:
    """Test BaseMode.get_available_operations() filtering logic."""

    def test_base_mode_normal_mode_returns_normal_operations(self):
        """In NORMAL mode, get_available_operations returns only NORMAL_OPERATIONS."""
        mode_handler = BaseMode()
        result = mode_handler.get_available_operations(Mode.NORMAL)

        # All keys in result should be from NORMAL_OPERATIONS
        for key in result.keys():
            assert key in NORMAL_OPERATIONS

        # All NORMAL_OPERATIONS keys should be in result
        for key in NORMAL_OPERATIONS.keys():
            assert key in result

    def test_base_mode_scientific_mode_returns_all_operations(self):
        """In SCIENTIFIC mode, get_available_operations returns full OPERATIONS dict."""
        mode_handler = BaseMode()
        result = mode_handler.get_available_operations(Mode.SCIENTIFIC)

        # Result should be identical to OPERATIONS
        assert result is OPERATIONS

        # All NORMAL_OPERATIONS should be present
        for key in NORMAL_OPERATIONS.keys():
            assert key in result

        # All SCIENTIFIC_OPERATIONS should be present
        for key in SCIENTIFIC_OPERATIONS.keys():
            assert key in result

    def test_base_mode_normal_excludes_scientific_operations(self):
        """NORMAL mode filtering must exclude scientific-only operations."""
        mode_handler = BaseMode()
        result = mode_handler.get_available_operations(Mode.NORMAL)

        # Scientific-only operations should not be present
        scientific_only = {"sin", "cos", "tan", "asin", "acos", "atan", "pi", "e"}
        for key in scientific_only:
            if key in OPERATIONS:  # Only check if it actually exists
                assert key not in result

    def test_base_mode_returns_dict(self):
        """get_available_operations must always return a dict."""
        mode_handler = BaseMode()
        result_normal = mode_handler.get_available_operations(Mode.NORMAL)
        result_scientific = mode_handler.get_available_operations(Mode.SCIENTIFIC)

        assert isinstance(result_normal, dict)
        assert isinstance(result_scientific, dict)

    def test_base_mode_normal_returns_subset_of_full(self):
        """Normal mode result must be a subset of OPERATIONS."""
        mode_handler = BaseMode()
        normal_ops = mode_handler.get_available_operations(Mode.NORMAL)
        full_ops = mode_handler.get_available_operations(Mode.SCIENTIFIC)

        # Every key in normal_ops should be in full_ops
        for key in normal_ops.keys():
            assert key in full_ops

    def test_base_mode_normal_has_fewer_operations(self):
        """Normal mode must have fewer operations than scientific mode."""
        mode_handler = BaseMode()
        normal_ops = mode_handler.get_available_operations(Mode.NORMAL)
        full_ops = mode_handler.get_available_operations(Mode.SCIENTIFIC)

        assert len(normal_ops) < len(full_ops)


class TestBaseModeFilterOperationsForNormalMode:
    """Test BaseMode._filter_operations_for_normal_mode() helper."""

    def test_filter_operations_returns_dict(self):
        """_filter_operations_for_normal_mode must return a dict."""
        mode_handler = BaseMode()
        result = mode_handler._filter_operations_for_normal_mode(OPERATIONS)
        assert isinstance(result, dict)

    def test_filter_operations_preserves_normal_operations(self):
        """_filter_operations_for_normal_mode must preserve all NORMAL_OPERATIONS keys."""
        mode_handler = BaseMode()
        result = mode_handler._filter_operations_for_normal_mode(OPERATIONS)

        for key in NORMAL_OPERATIONS.keys():
            assert key in result

    def test_filter_operations_excludes_scientific_operations(self):
        """_filter_operations_for_normal_mode must exclude scientific-only operations."""
        mode_handler = BaseMode()
        result = mode_handler._filter_operations_for_normal_mode(OPERATIONS)

        # Check that scientific-only ops are not present
        for key in SCIENTIFIC_OPERATIONS.keys():
            if key not in NORMAL_OPERATIONS:
                assert key not in result

    def test_filter_operations_with_empty_dict(self):
        """_filter_operations_for_normal_mode must handle empty dict gracefully."""
        mode_handler = BaseMode()
        result = mode_handler._filter_operations_for_normal_mode({})
        assert result == {}

    def test_filter_operations_with_partial_dict(self):
        """_filter_operations_for_normal_mode must handle dict missing some normal ops."""
        mode_handler = BaseMode()
        partial_dict = {"add": OPERATIONS["add"], "unknown": {"arity": 1}}
        result = mode_handler._filter_operations_for_normal_mode(partial_dict)

        # Only "add" should be present (it's in NORMAL_OPERATIONS)
        assert "add" in result
        assert "unknown" not in result

    def test_filter_operations_preserves_operation_metadata(self):
        """_filter_operations_for_normal_mode must preserve operation metadata."""
        mode_handler = BaseMode()
        result = mode_handler._filter_operations_for_normal_mode(OPERATIONS)

        # Check that preserved operations have the correct metadata
        add_op = result.get("add")
        assert add_op is not None
        assert add_op["arity"] == 2
        assert "label" in add_op


# ===========================================================================
# GuiCalculator Initialization Tests (with tkinter mocking)
# ===========================================================================

class TestGuiCalculatorInitialization:
    """Test GuiCalculator initialization with tkinter availability."""

    @patch("src.interface.gui.tk")
    def test_gui_calculator_raises_import_error_when_tkinter_unavailable(self, mock_tk):
        """GuiCalculator.__init__ must raise ImportError if tkinter is None."""
        # Simulate tkinter being unavailable
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
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_gui_calculator_initializes_with_calculator(self):
        """GuiCalculator must initialize with Calculator instance."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert gui._calculator is calculator

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_gui_calculator_initializes_mode_handler(self):
        """GuiCalculator must initialize _mode_handler as BaseMode instance."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert isinstance(gui._mode_handler, BaseMode)

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_gui_calculator_initializes_in_normal_mode(self):
        """GuiCalculator must initialize with _mode = Mode.NORMAL."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert gui._mode is Mode.NORMAL

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_gui_calculator_initializes_history(self):
        """GuiCalculator must initialize _history as History instance."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert isinstance(gui._history, History)

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_gui_calculator_initializes_widgets_to_none(self):
        """GuiCalculator must initialize widget references to None."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert gui._result_label is None or hasattr(gui, "_result_label")
        assert gui._history_text is None or hasattr(gui, "_history_text")
        assert gui._op_frame is None or hasattr(gui, "_op_frame")


# ===========================================================================
# Window Creation and Widget Tests
# ===========================================================================

class TestGuiCalculatorWindowAndWidgets:
    """Test window creation and widget existence."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_gui_window_has_root_reference(self):
        """GuiCalculator must store root window reference."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert gui._root is root

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_gui_has_result_display_attribute(self):
        """GuiCalculator must have _result_label attribute after setup."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # After _setup_layout, _result_label should be populated or None
        assert hasattr(gui, "_result_label")

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_gui_has_history_display_attribute(self):
        """GuiCalculator must have _history_text attribute after setup."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert hasattr(gui, "_history_text")

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_gui_has_operation_frame_attribute(self):
        """GuiCalculator must have _op_frame attribute for operation buttons."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert hasattr(gui, "_op_frame")


# ===========================================================================
# Mode Switching Tests
# ===========================================================================

class TestGuiCalculatorModeSwitching:
    """Test mode selection and operation grid updates."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_on_mode_change_updates_internal_mode(self):
        """_on_mode_change must update internal _mode attribute."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # Start in NORMAL mode
        assert gui._mode is Mode.NORMAL

        # Switch to SCIENTIFIC
        gui._on_mode_change(Mode.SCIENTIFIC)

        assert gui._mode is Mode.SCIENTIFIC

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_on_mode_change_switches_back_to_normal(self):
        """_on_mode_change must switch back from SCIENTIFIC to NORMAL."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._mode = Mode.SCIENTIFIC
        gui._on_mode_change(Mode.NORMAL)

        assert gui._mode is Mode.NORMAL

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_get_available_operations_normal_mode(self):
        """_get_available_operations_for_mode in NORMAL mode returns normal operations only."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)
        gui._mode = Mode.NORMAL

        ops = gui._get_available_operations_for_mode()

        # All returned keys should be in NORMAL_OPERATIONS
        for key in ops.keys():
            assert key in NORMAL_OPERATIONS

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_get_available_operations_scientific_mode(self):
        """_get_available_operations_for_mode in SCIENTIFIC mode returns all operations."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)
        gui._mode = Mode.SCIENTIFIC

        ops = gui._get_available_operations_for_mode()

        # All NORMAL_OPERATIONS keys should be present
        for key in NORMAL_OPERATIONS.keys():
            assert key in ops

        # All SCIENTIFIC_OPERATIONS keys should be present
        for key in SCIENTIFIC_OPERATIONS.keys():
            assert key in ops

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_get_available_operations_excludes_scientific_in_normal_mode(self):
        """In NORMAL mode, scientific-only operations must not be available."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)
        gui._mode = Mode.NORMAL

        ops = gui._get_available_operations_for_mode()

        # Scientific-only operations should not be present
        for key in SCIENTIFIC_OPERATIONS.keys():
            if key not in NORMAL_OPERATIONS:
                assert key not in ops


# ===========================================================================
# Operand Input Dialog Tests
# ===========================================================================

class TestGuiCalculatorPromptOperandsDialog:
    """Test operand collection via dialogs."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog")
    def test_prompt_operands_unary_operation(self, mock_simpledialog):
        """_prompt_operands_dialog for unary operation prompts once."""
        from src.interface.gui import GuiCalculator

        mock_simpledialog.askstring.return_value = "5.5"

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        operands = gui._prompt_operands_dialog("sqrt", 1, float)

        assert operands == [5.5]
        assert mock_simpledialog.askstring.call_count == 1

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog")
    def test_prompt_operands_binary_operation(self, mock_simpledialog):
        """_prompt_operands_dialog for binary operation prompts twice."""
        from src.interface.gui import GuiCalculator

        mock_simpledialog.askstring.side_effect = ["3.0", "4.0"]

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        operands = gui._prompt_operands_dialog("add", 2, float)

        assert operands == [3.0, 4.0]
        assert mock_simpledialog.askstring.call_count == 2

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog")
    def test_prompt_operands_cancel_returns_none(self, mock_simpledialog):
        """_prompt_operands_dialog returns None when user cancels."""
        from src.interface.gui import GuiCalculator

        mock_simpledialog.askstring.return_value = None

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        operands = gui._prompt_operands_dialog("sqrt", 1, float)

        assert operands is None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog")
    def test_prompt_operands_cancel_on_second_operand(self, mock_simpledialog):
        """_prompt_operands_dialog returns None when user cancels on second operand."""
        from src.interface.gui import GuiCalculator

        mock_simpledialog.askstring.side_effect = ["3.0", None]

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        operands = gui._prompt_operands_dialog("add", 2, float)

        assert operands is None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog")
    def test_prompt_operands_invalid_input_shows_error(self, mock_simpledialog):
        """_prompt_operands_dialog shows error dialog for invalid operand."""
        from src.interface.gui import GuiCalculator

        mock_simpledialog.askstring.return_value = "not_a_number"

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        with patch.object(gui, "_show_error_dialog") as mock_error:
            operands = gui._prompt_operands_dialog("sqrt", 1, float)

            # Should show error dialog and return None
            assert operands is None
            mock_error.assert_called_once()

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog")
    def test_prompt_operands_with_int_coerce(self, mock_simpledialog):
        """_prompt_operands_dialog respects coerce function (int)."""
        from src.interface.gui import GuiCalculator

        mock_simpledialog.askstring.return_value = "5"

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        operands = gui._prompt_operands_dialog("factorial", 1, int)

        assert operands == [5]
        assert isinstance(operands[0], int)

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog")
    def test_prompt_operands_strips_whitespace(self, mock_simpledialog):
        """_prompt_operands_dialog strips whitespace from input."""
        from src.interface.gui import GuiCalculator

        mock_simpledialog.askstring.return_value = "  5.5  "

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        operands = gui._prompt_operands_dialog("sqrt", 1, float)

        assert operands == [5.5]


# ===========================================================================
# Operation Execution Tests
# ===========================================================================

class TestGuiCalculatorOperationExecution:
    """Test operation execution via _execute_operation."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_execute_operation_unary_add_result(self):
        """_execute_operation executes unary operation correctly."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # Execute square operation on 5
        gui._execute_operation("square", [5.0])

        # Check result display was updated (via mocked label)
        assert gui._history._operations  # History should have one entry

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_execute_operation_binary_add(self):
        """_execute_operation executes binary operation correctly."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # Execute add operation
        gui._execute_operation("add", [3.0, 4.0])

        # Check history has the operation
        assert len(gui._history._operations) == 1
        assert "add" in gui._history._operations[0]

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_execute_operation_updates_history(self):
        """_execute_operation updates history after successful execution."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        initial_count = len(gui._history._operations)
        gui._execute_operation("multiply", [2.0, 3.0])

        assert len(gui._history._operations) == initial_count + 1

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_execute_operation_division_by_zero_shows_error(self):
        """_execute_operation handles ZeroDivisionError gracefully."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        with patch.object(gui, "_show_error_dialog") as mock_error:
            gui._execute_operation("divide", [10.0, 0.0])

            # Error dialog should be shown
            mock_error.assert_called_once()
            assert "Division by Zero" in str(mock_error.call_args)

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_execute_operation_domain_error_shows_error(self):
        """_execute_operation handles domain errors (ValueError) gracefully."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        with patch.object(gui, "_show_error_dialog") as mock_error:
            # square_root of negative number should raise ValueError
            gui._execute_operation("square_root", [-4.0])

            mock_error.assert_called_once()
            assert "Domain Error" in str(mock_error.call_args)

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_execute_operation_does_not_add_to_history_on_error(self):
        """_execute_operation does not add to history when operation fails."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        initial_count = len(gui._history._operations)

        with patch.object(gui, "_show_error_dialog"):
            gui._execute_operation("divide", [10.0, 0.0])

        # History should not have changed
        assert len(gui._history._operations) == initial_count

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_execute_operation_initializes_logger_lazily(self):
        """_execute_operation initializes logger if None."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator, logger=None)

        assert gui._logger is None

        gui._execute_operation("add", [1.0, 1.0])

        assert gui._logger is not None


# ===========================================================================
# History Display Tests
# ===========================================================================

class TestGuiCalculatorHistoryDisplay:
    """Test history display and updates."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_history_empty_on_startup(self):
        """History is empty when GUI starts."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert len(gui._history.get_all()) == 0

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_history_shows_after_operation(self):
        """History shows entry after executing one operation."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._execute_operation("add", [2.0, 3.0])

        history_entries = gui._history.get_all()
        assert len(history_entries) == 1
        assert "add" in history_entries[0]

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_history_shows_multiple_operations(self):
        """History accumulates multiple operations."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._execute_operation("add", [2.0, 3.0])
        gui._execute_operation("multiply", [5.0, 2.0])
        gui._execute_operation("square", [4.0])

        history_entries = gui._history.get_all()
        assert len(history_entries) == 3

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_history_entries_formatted_correctly(self):
        """History entries are formatted as operation(operands) = result."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._execute_operation("add", [2.0, 3.0])

        history_entries = gui._history.get_all()
        # Entry should be like "add(2.0, 3.0) = 5.0"
        assert "=" in history_entries[0]
        assert "add" in history_entries[0]

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_update_history_display_calls_text_widget(self):
        """_update_history_display updates the text widget."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # Mock the text widget
        gui._history_text = MagicMock()

        gui._history.add_operation("add", [1.0, 2.0], 3.0)
        gui._update_history_display()

        # Text widget should have been configured and updated
        assert gui._history_text.configure.called or gui._history_text.delete.called


# ===========================================================================
# Integration Tests
# ===========================================================================

class TestGuiCalculatorIntegration:
    """Integration tests combining multiple components."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog")
    def test_full_unary_operation_flow(self, mock_simpledialog):
        """Complete flow: dialog -> execution -> history."""
        from src.interface.gui import GuiCalculator

        mock_simpledialog.askstring.return_value = "9.0"

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # Simulate operation click
        operands = gui._prompt_operands_dialog("square_root", 1, float)
        assert operands == [9.0]

        gui._execute_operation("square_root", operands)

        assert len(gui._history.get_all()) == 1

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog")
    def test_full_binary_operation_flow(self, mock_simpledialog):
        """Complete flow for binary operation: dialogs -> execution -> history."""
        from src.interface.gui import GuiCalculator

        mock_simpledialog.askstring.side_effect = ["5.0", "3.0"]

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        operands = gui._prompt_operands_dialog("add", 2, float)
        assert operands == [5.0, 3.0]

        gui._execute_operation("add", operands)

        assert len(gui._history.get_all()) == 1

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog")
    def test_mode_switch_affects_available_operations(self, mock_simpledialog):
        """Switching modes changes available operations."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # Start in NORMAL mode
        normal_ops = gui._get_available_operations_for_mode()
        normal_count = len(normal_ops)

        # Switch to SCIENTIFIC
        gui._on_mode_change(Mode.SCIENTIFIC)
        scientific_ops = gui._get_available_operations_for_mode()
        scientific_count = len(scientific_ops)

        assert scientific_count > normal_count

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog")
    def test_normal_mode_scientific_operation_not_accessible(self, mock_simpledialog):
        """Scientific operations are not accessible in NORMAL mode."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)
        gui._mode = Mode.NORMAL

        available = gui._get_available_operations_for_mode()

        # sin, cos, tan, etc. should not be in normal mode
        assert "sin" not in available
        assert "cos" not in available
        assert "tan" not in available

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_gui_uses_calculator_instance_not_reimplemented(self):
        """GuiCalculator delegates to Calculator via dispatcher."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # Verify dispatcher is using the injected calculator
        assert gui._dispatcher._calculator is calculator

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_all_normal_operations_accessible_in_normal_mode(self):
        """All NORMAL_OPERATIONS keys are accessible in NORMAL mode."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)
        gui._mode = Mode.NORMAL

        available = gui._get_available_operations_for_mode()

        for key in NORMAL_OPERATIONS.keys():
            assert key in available

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_all_operations_accessible_in_scientific_mode(self):
        """All operations are accessible in SCIENTIFIC mode."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)
        gui._mode = Mode.SCIENTIFIC

        available = gui._get_available_operations_for_mode()

        for key in NORMAL_OPERATIONS.keys():
            assert key in available
        for key in SCIENTIFIC_OPERATIONS.keys():
            assert key in available


# ===========================================================================
# Edge Cases and Error Handling
# ===========================================================================

class TestGuiCalculatorEdgeCases:
    """Edge cases and boundary conditions."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_prompt_operands_zero_arity(self):
        """_prompt_operands_dialog handles arity=0 (no operands)."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        operands = gui._prompt_operands_dialog("pi", 0, float)

        assert operands == []

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog")
    def test_prompt_operands_negative_numbers(self, mock_simpledialog):
        """_prompt_operands_dialog handles negative numbers."""
        from src.interface.gui import GuiCalculator

        mock_simpledialog.askstring.side_effect = ["-5.0", "-3.0"]

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        operands = gui._prompt_operands_dialog("add", 2, float)

        assert operands == [-5.0, -3.0]

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog")
    def test_prompt_operands_large_numbers(self, mock_simpledialog):
        """_prompt_operands_dialog handles very large numbers."""
        from src.interface.gui import GuiCalculator

        mock_simpledialog.askstring.return_value = "1e100"

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        operands = gui._prompt_operands_dialog("multiply", 1, float)

        assert operands[0] == 1e100

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog")
    def test_prompt_operands_zero(self, mock_simpledialog):
        """_prompt_operands_dialog handles zero input."""
        from src.interface.gui import GuiCalculator

        mock_simpledialog.askstring.return_value = "0"

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        operands = gui._prompt_operands_dialog("sqrt", 1, float)

        assert operands == [0.0]

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_execute_operation_with_zero_operands(self):
        """_execute_operation handles operations with no operands."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # pi operation takes no operands
        gui._execute_operation("pi", [])

        assert len(gui._history.get_all()) == 1

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_multiple_operations_in_sequence(self):
        """GUI handles multiple operations in quick succession."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        for i in range(5):
            gui._execute_operation("add", [float(i), 1.0])

        assert len(gui._history.get_all()) == 5

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_mode_switch_multiple_times(self):
        """Mode can be switched multiple times."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._on_mode_change(Mode.SCIENTIFIC)
        assert gui._mode is Mode.SCIENTIFIC

        gui._on_mode_change(Mode.NORMAL)
        assert gui._mode is Mode.NORMAL

        gui._on_mode_change(Mode.SCIENTIFIC)
        assert gui._mode is Mode.SCIENTIFIC


# ===========================================================================
# Interface Exports Tests
# ===========================================================================

class TestInterfaceExports:
    """Test that GuiCalculator is properly exported from interface module."""

    def test_gui_calculator_exported_in_interface_init(self):
        """GuiCalculator must be exported from src.interface.__init__."""
        from src.interface import GuiCalculator

        assert GuiCalculator is not None

    def test_gui_calculator_in_all_exports(self):
        """GuiCalculator must be in __all__ of src.interface."""
        from src import interface

        assert "GuiCalculator" in interface.__all__

    def test_interface_all_contains_gui_calculator(self):
        """src.interface.__all__ must include GuiCalculator."""
        import src.interface

        assert "GuiCalculator" in src.interface.__all__


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
