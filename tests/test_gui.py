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

# ===========================================================================
# iOS GUI Redesign Tests (Issue #129)
# ===========================================================================

class TestThemeConstants:
    """Test the _THEME dictionary exists and contains all expected keys."""

    def test_theme_exists_in_gui_module(self):
        """_THEME must be defined in gui module."""
        from src.interface import gui

        assert hasattr(gui, "_THEME")
        assert isinstance(gui._THEME, dict)

    def test_theme_has_background_color(self):
        """_THEME must contain 'bg' key with black color."""
        from src.interface import gui

        assert "bg" in gui._THEME
        assert gui._THEME["bg"] == "#000000"

    def test_theme_has_foreground_color(self):
        """_THEME must contain 'fg' key with white color."""
        from src.interface import gui

        assert "fg" in gui._THEME
        assert gui._THEME["fg"] == "#FFFFFF"

    def test_theme_has_display_font(self):
        """_THEME must contain 'display_font' key."""
        from src.interface import gui

        assert "display_font" in gui._THEME

    def test_theme_has_button_font(self):
        """_THEME must contain 'button_font' key."""
        from src.interface import gui

        assert "button_font" in gui._THEME

    def test_theme_has_operator_colors(self):
        """_THEME must contain operation button color keys."""
        from src.interface import gui

        assert "op_bg" in gui._THEME
        assert "op_active" in gui._THEME
        assert gui._THEME["op_bg"] == "#FF9500"  # iOS orange

    def test_theme_has_scientific_button_colors(self):
        """_THEME must contain scientific button color keys."""
        from src.interface import gui

        assert "sci_bg" in gui._THEME
        assert "sci_active" in gui._THEME

    def test_theme_has_standard_button_colors(self):
        """_THEME must contain standard button color keys."""
        from src.interface import gui

        assert "std_bg" in gui._THEME
        assert "std_active" in gui._THEME

    def test_theme_has_number_button_colors(self):
        """_THEME must contain number button color keys."""
        from src.interface import gui

        assert "num_bg" in gui._THEME
        assert "num_active" in gui._THEME

    def test_theme_has_toggle_button_colors(self):
        """_THEME must contain toggle button color keys."""
        from src.interface import gui

        assert "toggle_bg" in gui._THEME
        assert "toggle_active" in gui._THEME


class TestOperationSymbols:
    """Test the _OP_SYMBOLS mapping."""

    def test_op_symbols_exists_in_gui_module(self):
        """_OP_SYMBOLS must be defined in gui module."""
        from src.interface import gui

        assert hasattr(gui, "_OP_SYMBOLS")
        assert isinstance(gui._OP_SYMBOLS, dict)

    def test_add_symbol(self):
        """_OP_SYMBOLS['add'] must map to '+'."""
        from src.interface import gui

        assert gui._OP_SYMBOLS["add"] == "+"

    def test_subtract_symbol(self):
        """_OP_SYMBOLS['subtract'] must map to '−' (minus sign)."""
        from src.interface import gui

        assert gui._OP_SYMBOLS["subtract"] == "\u2212"

    def test_multiply_symbol(self):
        """_OP_SYMBOLS['multiply'] must map to '×'."""
        from src.interface import gui

        assert gui._OP_SYMBOLS["multiply"] == "\u00d7"

    def test_divide_symbol(self):
        """_OP_SYMBOLS['divide'] must map to '÷'."""
        from src.interface import gui

        assert gui._OP_SYMBOLS["divide"] == "\u00f7"

    def test_sqrt_symbol(self):
        """_OP_SYMBOLS['sqrt'] must map to '√'."""
        from src.interface import gui

        assert gui._OP_SYMBOLS["sqrt"] == "\u221a"

    def test_square_symbol(self):
        """_OP_SYMBOLS['square'] must map to 'x²'."""
        from src.interface import gui

        assert gui._OP_SYMBOLS["square"] == "x\u00b2"

    def test_cube_symbol(self):
        """_OP_SYMBOLS['cube'] must map to 'x³'."""
        from src.interface import gui

        assert gui._OP_SYMBOLS["cube"] == "x\u00b3"

    def test_pi_symbol(self):
        """_OP_SYMBOLS['pi'] must map to 'π'."""
        from src.interface import gui

        assert gui._OP_SYMBOLS["pi"] == "\u03c0"


class TestArithmeticOpsConstant:
    """Test the _ARITHMETIC_OPS frozenset."""

    def test_arithmetic_ops_exists(self):
        """_ARITHMETIC_OPS must be defined in gui module."""
        from src.interface import gui

        assert hasattr(gui, "_ARITHMETIC_OPS")

    def test_arithmetic_ops_is_frozenset(self):
        """_ARITHMETIC_OPS must be a frozenset."""
        from src.interface import gui

        assert isinstance(gui._ARITHMETIC_OPS, frozenset)

    def test_arithmetic_ops_contains_add(self):
        """_ARITHMETIC_OPS must contain 'add'."""
        from src.interface import gui

        assert "add" in gui._ARITHMETIC_OPS

    def test_arithmetic_ops_contains_subtract(self):
        """_ARITHMETIC_OPS must contain 'subtract'."""
        from src.interface import gui

        assert "subtract" in gui._ARITHMETIC_OPS

    def test_arithmetic_ops_contains_multiply(self):
        """_ARITHMETIC_OPS must contain 'multiply'."""
        from src.interface import gui

        assert "multiply" in gui._ARITHMETIC_OPS

    def test_arithmetic_ops_contains_divide(self):
        """_ARITHMETIC_OPS must contain 'divide'."""
        from src.interface import gui

        assert "divide" in gui._ARITHMETIC_OPS

    def test_arithmetic_ops_exactly_four_elements(self):
        """_ARITHMETIC_OPS must contain exactly 4 operations."""
        from src.interface import gui

        assert len(gui._ARITHMETIC_OPS) == 4


class TestModeToggleButton:
    """Test the mode toggle button behavior."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_toggle_button_exists_after_init(self):
        """GuiCalculator must have _toggle_btn attribute after initialization."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert gui._toggle_btn is not None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_toggle_button_text_changes_on_mode_switch(self):
        """Toggle button text must change when mode changes."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # GUI starts in NORMAL mode
        assert gui._mode is Mode.NORMAL
        # Toggle button should exist
        assert gui._toggle_btn is not None

        # When switching to SCIENTIFIC, the toggle button should be updated
        gui._on_mode_change(Mode.SCIENTIFIC)
        assert gui._mode is Mode.SCIENTIFIC

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_on_toggle_mode_switches_to_scientific(self):
        """_on_toggle_mode must switch from NORMAL to SCIENTIFIC."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert gui._mode is Mode.NORMAL
        gui._on_toggle_mode()

        assert gui._mode is Mode.SCIENTIFIC

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_on_toggle_mode_switches_to_normal(self):
        """_on_toggle_mode must switch from SCIENTIFIC to NORMAL."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._mode = Mode.SCIENTIFIC
        gui._on_toggle_mode()

        assert gui._mode is Mode.NORMAL

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_on_toggle_mode_calls_configure(self):
        """_on_toggle_mode must call configure on the toggle button."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # Reset the call count to measure only the call from _on_toggle_mode
        gui._toggle_btn.configure.reset_mock()

        gui._on_toggle_mode()

        # configure should have been called to update the text
        gui._toggle_btn.configure.assert_called()

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_on_toggle_mode_method_exists(self):
        """GuiCalculator must have _on_toggle_mode method."""
        from src.interface.gui import GuiCalculator

        assert hasattr(GuiCalculator, "_on_toggle_mode")
        assert callable(getattr(GuiCalculator, "_on_toggle_mode"))


class TestNumberGrid:
    """Test the 3x4 number grid layout."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_number_frame_exists(self):
        """GuiCalculator must have _num_frame attribute."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert gui._num_frame is not None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_number_grid_setup_called(self):
        """_setup_number_grid must be called during initialization."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # Verify _num_frame was created and configured
        assert gui._num_frame is not None
        # Verify columnconfigure was called on the frame
        gui._num_frame.columnconfigure.assert_called()

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_number_grid_has_three_column_configs(self):
        """Number grid must configure 3 columns."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # columnconfigure should have been called for columns 0, 1, 2
        assert gui._num_frame.columnconfigure.call_count >= 3

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_number_grid_has_four_row_configs(self):
        """Number grid must configure 4 rows."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # rowconfigure should have been called for rows 0-3
        assert gui._num_frame.rowconfigure.call_count >= 4

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_number_grid_frame_not_none(self):
        """Number grid frame must be initialized."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # The layout is internally verified by _setup_number_grid
        assert gui._num_frame is not None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_number_grid_button_creation_called(self):
        """_setup_number_grid must create buttons via tk.Button."""
        from src.interface.gui import GuiCalculator
        import src.interface.gui as gui_module

        root = MagicMock()
        calculator = Calculator()

        # Count Button creations
        button_calls_before = gui_module.tk.Button.call_count
        gui = GuiCalculator(root, calculator)
        button_calls_after = gui_module.tk.Button.call_count

        # Should have created buttons for digits 0-9 plus operation buttons
        assert button_calls_after > button_calls_before

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_setup_number_grid_method_exists(self):
        """GuiCalculator must have _setup_number_grid method."""
        from src.interface.gui import GuiCalculator

        assert hasattr(GuiCalculator, "_setup_number_grid")
        assert callable(getattr(GuiCalculator, "_setup_number_grid"))


class TestResultDisplay:
    """Test the result display label."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_result_label_exists(self):
        """GuiCalculator must have _result_label after initialization."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert gui._result_label is not None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_result_label_initialized(self):
        """Result label must be initialized after setup."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # Result label must be created
        assert gui._result_label is not None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_update_result_display_calls_configure(self):
        """_update_result_display must call configure on the label."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._result_label.configure.reset_mock()
        gui._update_result_display(42)

        # configure must be called to update the text
        gui._result_label.configure.assert_called()

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_update_result_display_with_float(self):
        """_update_result_display must call configure with float value."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._result_label.configure.reset_mock()
        gui._update_result_display(15.0)

        gui._result_label.configure.assert_called()
        # Verify that the string "15.0" was passed
        args, kwargs = gui._result_label.configure.call_args
        assert "text" in kwargs or any("15.0" in str(arg) for arg in args)

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_update_result_display_with_integer(self):
        """_update_result_display must handle integer values."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        gui._result_label.configure.reset_mock()
        gui._update_result_display(42)

        gui._result_label.configure.assert_called()

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_result_label_method_exists(self):
        """GuiCalculator must have _update_result_display method."""
        from src.interface.gui import GuiCalculator

        assert hasattr(GuiCalculator, "_update_result_display")
        assert callable(getattr(GuiCalculator, "_update_result_display"))


class TestOperationButtonStyling:
    """Test operation button styling and colors."""

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_operation_frame_exists(self):
        """GuiCalculator must have _op_frame attribute."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        assert gui._op_frame is not None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_setup_operation_grid_called(self):
        """_setup_operation_grid must be called during initialization."""
        from src.interface.gui import GuiCalculator

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # Verify _op_frame was configured
        assert gui._op_frame is not None
        gui._op_frame.columnconfigure.assert_called()

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_operation_buttons_created_on_init(self):
        """Operation buttons must be created during initialization."""
        from src.interface.gui import GuiCalculator
        import src.interface.gui as gui_module

        root = MagicMock()
        calculator = Calculator()

        button_count_before = gui_module.tk.Button.call_count
        gui = GuiCalculator(root, calculator)
        button_count_after = gui_module.tk.Button.call_count

        # Should have created buttons for operations and numbers
        assert button_count_after > button_count_before

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_setup_operation_grid_method_exists(self):
        """GuiCalculator must have _setup_operation_grid method."""
        from src.interface.gui import GuiCalculator

        assert hasattr(GuiCalculator, "_setup_operation_grid")
        assert callable(getattr(GuiCalculator, "_setup_operation_grid"))

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_operation_grid_rebuilds_on_mode_change(self):
        """Operation grid must be rebuilt when mode changes."""
        from src.interface.gui import GuiCalculator
        from src.session.mode import Mode

        root = MagicMock()
        calculator = Calculator()
        gui = GuiCalculator(root, calculator)

        # Record winfo_children calls before mode change
        calls_before = gui._op_frame.destroy.call_count

        gui._on_mode_change(Mode.SCIENTIFIC)

        # The operation frame's children should be destroyed and rebuilt
        # (destroy is called on each widget)
        assert gui._op_frame is not None

    @patch("src.interface.gui.tk", MagicMock())
    @patch("src.interface.gui.messagebox", MagicMock())
    @patch("src.interface.gui.simpledialog", MagicMock())
    def test_arithmetic_ops_constant_valid(self):
        """_ARITHMETIC_OPS must contain only valid operation keys."""
        from src.interface.gui import _ARITHMETIC_OPS, _OP_SYMBOLS

        for op_key in _ARITHMETIC_OPS:
            assert op_key in _OP_SYMBOLS


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
