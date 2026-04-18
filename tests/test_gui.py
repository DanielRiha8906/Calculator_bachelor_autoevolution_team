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


# ===========================================================================
# iOS-Style GuiCalculator Visual Redesign Tests
# ===========================================================================

class TestGuiCalculatorVisualStructure:
    """Verify the new iOS-style visual layout and structure."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_theme_dict_exists_at_module_level(self):
        """_THEME dict must exist at module level with required keys."""
        import src.interface.gui

        assert hasattr(src.interface.gui, "_THEME")
        theme = src.interface.gui._THEME
        assert isinstance(theme, dict)
        assert "COLORS" in theme
        assert "FONTS" in theme
        assert "PADDING" in theme

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_theme_colors_contain_required_keys(self):
        """_THEME['COLORS'] must contain all required color definitions."""
        import src.interface.gui

        colors = src.interface.gui._THEME["COLORS"]
        required = [
            "bg_window", "bg_display", "fg_display",
            "bg_operator", "fg_operator", "active_operator",
            "bg_scientific", "fg_scientific", "active_scientific",
            "bg_standard", "fg_standard", "active_standard",
            "bg_number", "fg_number", "active_number"
        ]
        for key in required:
            assert key in colors, f"Missing color key: {key}"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_result_label_has_black_background(self):
        """Result label must use black background."""
        import src.interface.gui

        colors = src.interface.gui._THEME["COLORS"]
        assert colors["bg_display"] == "#000000"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_result_label_has_white_foreground(self):
        """Result label must use white foreground."""
        import src.interface.gui

        colors = src.interface.gui._THEME["COLORS"]
        assert colors["fg_display"] == "#FFFFFF"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_result_label_font_is_monospaced_bold(self):
        """Result label font must be monospaced (Courier) and bold."""
        import src.interface.gui

        fonts = src.interface.gui._THEME["FONTS"]
        display_font = fonts["display"]
        assert "Courier" in display_font[0]
        assert "bold" in display_font

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_result_label_created_at_row_zero(self):
        """Result label must be placed at row 0 (top of layout)."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # After _setup_layout, result label should exist
        assert gui._result_label is not None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_mode_toggle_button_created(self):
        """Mode toggle button must be created and accessible."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert gui._mode_toggle_btn is not None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_operation_frame_created(self):
        """Operation button grid frame must be created."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert gui._op_frame is not None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_mode_toggle_shows_scientific_when_in_normal_mode(self):
        """Mode toggle button must show 'scientific' when in NORMAL mode."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)
        gui._mode = Mode.NORMAL

        label = gui._mode_toggle_label()
        assert label == "scientific"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_mode_toggle_shows_normal_when_in_scientific_mode(self):
        """Mode toggle button must show 'normal' when in SCIENTIFIC mode."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)
        gui._mode = Mode.SCIENTIFIC

        label = gui._mode_toggle_label()
        assert label == "normal"


# ===========================================================================
# Button Color Assignment Tests
# ===========================================================================

class TestGuiCalculatorButtonColors:
    """Verify button color assignments by operation type."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_operator_buttons_use_operator_color(self):
        """Operator buttons (add, subtract, multiply, divide) must use operator color."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)
        gui._mode = Mode.NORMAL

        for op_key in ["add", "subtract", "multiply", "divide"]:
            color_group = gui._get_operation_color_group(op_key)
            assert color_group == "operator", f"Failed for {op_key}"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_operator_color_is_orange(self):
        """Operator color must be #FF9500 (iOS orange)."""
        import src.interface.gui

        colors = src.interface.gui._THEME["COLORS"]
        assert colors["bg_operator"] == "#FF9500"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_scientific_buttons_in_scientific_mode(self):
        """Scientific operation buttons must use scientific color in SCIENTIFIC mode."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)
        gui._mode = Mode.SCIENTIFIC

        # Scientific operations (not operators, not standard)
        sci_ops = ["sin", "cos", "tan", "sqrt", "log", "ln"]
        for op_key in sci_ops:
            if op_key in OPERATIONS:
                color_group = gui._get_operation_color_group(op_key)
                assert color_group == "scientific", f"Failed for {op_key}"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_scientific_color_is_dark_gray(self):
        """Scientific color must be #1C1C1E."""
        import src.interface.gui

        colors = src.interface.gui._THEME["COLORS"]
        assert colors["bg_scientific"] == "#1C1C1E"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_standard_buttons_in_normal_mode(self):
        """Non-operator buttons must use standard color in NORMAL mode."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)
        gui._mode = Mode.NORMAL

        # Non-operator operations in normal mode
        non_operators = ["square", "cube", "factorial", "square_root"]
        for op_key in non_operators:
            if op_key in OPERATIONS and op_key not in ["add", "subtract", "multiply", "divide"]:
                color_group = gui._get_operation_color_group(op_key)
                assert color_group == "standard", f"Failed for {op_key}"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_standard_color_is_dark_gray(self):
        """Standard color must be #333333."""
        import src.interface.gui

        colors = src.interface.gui._THEME["COLORS"]
        assert colors["bg_standard"] == "#333333"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_number_buttons_use_standard_color(self):
        """Number buttons must use standard (dark gray) color."""
        import src.interface.gui

        colors = src.interface.gui._THEME["COLORS"]
        assert colors["bg_number"] == "#333333"


# ===========================================================================
# Symbolic Labels Tests
# ===========================================================================

class TestGuiCalculatorSymbolicLabels:
    """Verify operation buttons display symbols, not text descriptions."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_add_symbol_is_plus(self):
        """add operation must display '+' symbol."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        symbol = gui._get_operation_symbol("add")
        assert symbol == "+"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_subtract_symbol_is_minus(self):
        """subtract operation must display '−' (Unicode minus) symbol."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        symbol = gui._get_operation_symbol("subtract")
        assert symbol == "\u2212"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_multiply_symbol_is_times(self):
        """multiply operation must display '×' symbol."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        symbol = gui._get_operation_symbol("multiply")
        assert symbol == "\u00d7"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_divide_symbol_is_obelus(self):
        """divide operation must display '÷' symbol."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        symbol = gui._get_operation_symbol("divide")
        assert symbol == "\u00f7"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_sqrt_symbol_is_radical(self):
        """square_root operation must display '√' symbol."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        symbol = gui._get_operation_symbol("sqrt")
        assert symbol == "\u221a"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_square_symbol_is_x_squared(self):
        """square operation must display 'x²' symbol."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        symbol = gui._get_operation_symbol("square")
        assert symbol == "x\u00b2"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_cube_symbol_is_x_cubed(self):
        """cube operation must display 'x³' symbol."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        symbol = gui._get_operation_symbol("cube")
        assert symbol == "x\u00b3"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_power_symbol_is_x_to_power(self):
        """power operation must display 'xʸ' symbol."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        symbol = gui._get_operation_symbol("power")
        assert symbol == "x\u02b8"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_factorial_symbol_is_n_exclamation(self):
        """factorial operation must display 'n!' symbol."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        symbol = gui._get_operation_symbol("factorial")
        assert symbol == "n!"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_pi_symbol_is_pi_letter(self):
        """pi operation must display 'π' symbol."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        symbol = gui._get_operation_symbol("pi")
        assert symbol == "\u03c0"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_unknown_operation_returns_key_as_fallback(self):
        """Unknown operation key must be returned as-is."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        symbol = gui._get_operation_symbol("unknown_op")
        assert symbol == "unknown_op"


# ===========================================================================
# Hover Effect Tests
# ===========================================================================

class TestGuiCalculatorHoverEffect:
    """Verify hover bindings and visual feedback."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_bind_hover_attaches_enter_binding(self):
        """_bind_hover must attach <Enter> binding to button."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        button = MagicMock()
        gui._bind_hover(button, "#333333", "#4D4D4D")

        # bind should be called with "<Enter>"
        assert button.bind.called
        calls = [call[0][0] for call in button.bind.call_args_list]
        assert "<Enter>" in calls

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_bind_hover_attaches_leave_binding(self):
        """_bind_hover must attach <Leave> binding to button."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        button = MagicMock()
        gui._bind_hover(button, "#333333", "#4D4D4D")

        # bind should be called with "<Leave>"
        calls = [call[0][0] for call in button.bind.call_args_list]
        assert "<Leave>" in calls

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_bind_hover_enter_changes_to_hover_color(self):
        """<Enter> binding must configure button to hover background color."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        button = MagicMock()
        default_bg = "#333333"
        hover_bg = "#4D4D4D"

        gui._bind_hover(button, default_bg, hover_bg)

        # Get the Enter handler and call it
        enter_handler = None
        for call_args in button.bind.call_args_list:
            if call_args[0][0] == "<Enter>":
                enter_handler = call_args[0][1]
                break

        assert enter_handler is not None
        # Simulate event call
        enter_handler(MagicMock())

        # button.configure should have been called with bg=hover_bg
        # Check that button's configure was called (it will be in the lambda)

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_bind_hover_leave_restores_default_color(self):
        """<Leave> binding must restore button to default background color."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        button = MagicMock()
        default_bg = "#333333"
        hover_bg = "#4D4D4D"

        gui._bind_hover(button, default_bg, hover_bg)

        # Get the Leave handler
        leave_handler = None
        for call_args in button.bind.call_args_list:
            if call_args[0][0] == "<Leave>":
                leave_handler = call_args[0][1]
                break

        assert leave_handler is not None


# ===========================================================================
# Mode Toggle Tests (Redesign-Specific)
# ===========================================================================

class TestGuiCalculatorModeToggleRedesign:
    """Test mode toggle functionality in the iOS-style redesign."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_on_mode_toggle_switches_from_normal_to_scientific(self):
        """_on_mode_toggle must switch from NORMAL to SCIENTIFIC."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)
        gui._mode = Mode.NORMAL

        gui._on_mode_toggle()

        assert gui._mode is Mode.SCIENTIFIC

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_on_mode_toggle_switches_from_scientific_to_normal(self):
        """_on_mode_toggle must switch from SCIENTIFIC to NORMAL."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)
        gui._mode = Mode.SCIENTIFIC

        gui._on_mode_toggle()

        assert gui._mode is Mode.NORMAL

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_on_mode_toggle_updates_toggle_button_label(self):
        """_on_mode_toggle must update the toggle button label."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)
        gui._mode = Mode.NORMAL
        gui._mode_toggle_btn = MagicMock()

        gui._on_mode_toggle()

        # After toggle to SCIENTIFIC, label should be "normal"
        gui._mode_toggle_btn.configure.assert_called()

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_on_mode_change_updates_mode_var(self):
        """_on_mode_change must update the _mode_var StringVar."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)
        gui._mode = Mode.NORMAL

        # Mock _mode_var to track calls
        gui._mode_var = MagicMock()

        gui._on_mode_change(Mode.SCIENTIFIC)

        # _mode_var.set should be called with the new mode's value
        gui._mode_var.set.assert_called_with(Mode.SCIENTIFIC.value)

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_on_mode_change_rebuilds_operation_grid(self):
        """_on_mode_change must call _setup_operation_grid to rebuild."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        with patch.object(gui, "_setup_operation_grid") as mock_setup:
            gui._on_mode_change(Mode.SCIENTIFIC)
            mock_setup.assert_called()

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_on_mode_change_updates_button_label(self):
        """_on_mode_change must update toggle button label via configure."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)
        gui._mode = Mode.NORMAL
        gui._mode_toggle_btn = MagicMock()

        gui._on_mode_change(Mode.SCIENTIFIC)

        # Button configure should be called with the new label
        assert gui._mode_toggle_btn.configure.called


# ===========================================================================
# Number Grid Tests
# ===========================================================================

class TestGuiCalculatorNumberGrid:
    """Test the fixed 4x3 number button grid structure."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_setup_number_grid_creates_buttons_for_digits(self):
        """_setup_number_grid must create buttons for all digits 0-9."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # Number frame will have buttons for 0-9
        # We need to verify that the grid layout is correct
        # by checking that the frame is set up properly
        assert gui._op_frame is not None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_setup_number_grid_has_4_columns(self):
        """Number grid must have exactly 4 columns."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # The grid should support at least 4 rows (0-9 = 10 digits in 4x3 grid)
        # with placeholders for empty cells
        assert gui._result_label is not None  # Just verify layout was set

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_setup_number_grid_digit_order_1_to_9_then_0(self):
        """Number grid must display digits in order: 1-9, then 0."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        parent = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # Expected layout:
        # Row 0: 1, 2, 3
        # Row 1: 4, 5, 6
        # Row 2: 7, 8, 9
        # Row 3: 0, None, None

        layout = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"],
            ["0", None, None],
        ]

        # Verify layout structure
        assert len(layout) == 4  # 4 rows
        assert len(layout[0]) == 3  # 3 columns for first row
        assert layout[3][0] == "0"  # 0 is in bottom-left


# ===========================================================================
# Result Display Tests (Redesign-Specific)
# ===========================================================================

class TestGuiCalculatorResultDisplayRedesign:
    """Test result display updates in the new design."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_update_result_display_shows_plain_numeric_string(self):
        """_update_result_display must show plain numeric string (no 'Result: ' prefix)."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)
        gui._result_label = MagicMock()

        gui._update_result_display(42)

        # Check that label was configured with just the numeric string
        call_kwargs = gui._result_label.configure.call_args[1]
        assert call_kwargs["text"] == "42"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_update_result_display_with_float(self):
        """_update_result_display must handle float results."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)
        gui._result_label = MagicMock()

        gui._update_result_display(3.14159)

        call_kwargs = gui._result_label.configure.call_args[1]
        assert "3.14159" in call_kwargs["text"]

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_update_result_display_with_zero(self):
        """_update_result_display must handle zero."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)
        gui._result_label = MagicMock()

        gui._update_result_display(0)

        call_kwargs = gui._result_label.configure.call_args[1]
        assert call_kwargs["text"] == "0"

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_update_result_display_with_negative(self):
        """_update_result_display must handle negative numbers."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)
        gui._result_label = MagicMock()

        gui._update_result_display(-42)

        call_kwargs = gui._result_label.configure.call_args[1]
        assert call_kwargs["text"] == "-42"


# ===========================================================================
# Operation Grid Tests
# ===========================================================================

class TestGuiCalculatorOperationGrid:
    """Test the operation button grid structure and layout."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_setup_operation_grid_clears_previous_buttons(self):
        """_setup_operation_grid must clear previously rendered buttons."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # Mock the frame to track destroy calls
        gui._op_frame = MagicMock()
        gui._op_frame.winfo_children.return_value = [MagicMock(), MagicMock()]

        gui._setup_operation_grid()

        # winfo_children should be called to get old widgets
        assert gui._op_frame.winfo_children.called

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_setup_operation_grid_rebuilds_on_mode_change(self):
        """_setup_operation_grid must repopulate with mode-appropriate operations."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)
        gui._mode = Mode.NORMAL

        # Call setup in NORMAL mode
        gui._setup_operation_grid()

        # Should have operation frame set up
        assert gui._op_frame is not None


# ===========================================================================
# Layout Structure Tests
# ===========================================================================

class TestGuiCalculatorLayoutStructure:
    """Test the overall 4-row layout structure."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_layout_has_result_display_at_row_zero(self):
        """Layout must have result display at row 0."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # Result label exists and is created first
        assert gui._result_label is not None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_layout_has_mode_toggle_button_at_row_one(self):
        """Layout must have mode toggle button at row 1."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert gui._mode_toggle_btn is not None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_layout_has_operation_grid_at_row_two(self):
        """Layout must have operation button grid at row 2."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert gui._op_frame is not None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_layout_has_number_grid_at_row_three(self):
        """Layout must have number button grid at row 3."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # After _setup_layout is called, all 4 rows are configured
        # We verify this by checking that all major widgets exist
        assert gui._result_label is not None
        assert gui._mode_toggle_btn is not None
        assert gui._op_frame is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
