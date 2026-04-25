"""Test suite for GUIController (src.calculator.gui.controller module).

This module tests the GUIController class, which provides a business logic layer
for GUI applications. The controller is responsible for:
- Mode management (normal/scientific)
- Operation registry and availability
- Operation execution with error handling
- Session history tracking and clearing
- Operation arity querying

The GUIController is designed to work with any UI framework (tkinter, PyQt, etc.)
by providing a pure Python API that the UI layer can call.
"""

import pytest
from src.calculator.gui.controller import GUIController


class TestGUIControllerInitialization:
    """Test GUIController initialization with different modes."""

    def test_gui_controller_init_normal_mode(self):
        """GUIController initializes with normal mode, no exceptions."""
        controller = GUIController(mode="normal")
        assert controller is not None
        assert controller.get_current_mode() == "normal"

    def test_gui_controller_init_scientific_mode(self):
        """GUIController initializes with scientific mode, no exceptions."""
        controller = GUIController(mode="scientific")
        assert controller is not None
        assert controller.get_current_mode() == "scientific"


class TestGUIControllerOperationAvailability:
    """Test GUIController operation listing for each mode."""

    def test_gui_controller_get_available_operations_normal(self):
        """Controller in normal mode returns list of 13 operation names."""
        controller = GUIController(mode="normal")
        operations = controller.get_available_operations()
        assert isinstance(operations, list)
        assert len(operations) == 13
        # Normal mode should have these operations
        assert "add" in operations
        assert "subtract" in operations
        assert "multiply" in operations
        assert "divide" in operations
        assert "factorial" in operations

    def test_gui_controller_get_available_operations_scientific(self):
        """Controller in scientific mode returns list of 25 operation names."""
        controller = GUIController(mode="scientific")
        operations = controller.get_available_operations()
        assert isinstance(operations, list)
        assert len(operations) == 25
        # Scientific mode should have both normal operations and new ones
        assert "add" in operations
        assert "sin" in operations
        assert "cos" in operations


class TestGUIControllerModeSwitch:
    """Test GUIController mode switching behavior."""

    def test_gui_controller_switch_mode_normal_to_scientific(self):
        """Controller starts normal, switch_mode('scientific'), returns 25 operations."""
        controller = GUIController(mode="normal")
        assert len(controller.get_available_operations()) == 13
        controller.switch_mode("scientific")
        assert len(controller.get_available_operations()) == 25
        assert controller.get_current_mode() == "scientific"

    def test_gui_controller_switch_mode_scientific_to_normal(self):
        """Controller starts scientific, switch_mode('normal'), returns 13 operations."""
        controller = GUIController(mode="scientific")
        assert len(controller.get_available_operations()) == 25
        controller.switch_mode("normal")
        assert len(controller.get_available_operations()) == 13
        assert controller.get_current_mode() == "normal"

    def test_gui_controller_get_current_mode_normal(self):
        """Controller initialized with 'normal', get_current_mode() returns 'normal'."""
        controller = GUIController(mode="normal")
        assert controller.get_current_mode() == "normal"

    def test_gui_controller_get_current_mode_scientific(self):
        """Controller initialized with 'scientific', get_current_mode() returns 'scientific'."""
        controller = GUIController(mode="scientific")
        assert controller.get_current_mode() == "scientific"


class TestGUIControllerOperationExecution:
    """Test GUIController execute_operation() method for various operations."""

    @pytest.mark.parametrize("operands,expected_result", [
        ([2, 3], 5),
        ([10, 5], 15),
        ([0, 0], 0),
        ([-1, 1], 0),
        ([1.5, 2.5], 4.0),
    ])
    def test_gui_controller_execute_operation_add_variants(self, operands, expected_result):
        """execute_operation('add', operands) returns expected results for valid inputs."""
        controller = GUIController(mode="normal")
        result = controller.execute_operation("add", operands)
        assert result["success"] is True
        assert result["result"] == expected_result
        assert result["operation"] == "add"
        assert result["operands"] == operands

    def test_gui_controller_execute_operation_success_add(self):
        """execute_operation('add', [2, 3]) returns success dict with result 5."""
        controller = GUIController(mode="normal")
        result = controller.execute_operation("add", [2, 3])
        assert result["success"] is True
        assert result["result"] == 5
        assert result["operation"] == "add"
        assert result["operands"] == [2, 3]

    def test_gui_controller_execute_operation_success_factorial(self):
        """execute_operation('factorial', [5]) returns success dict with result 120."""
        controller = GUIController(mode="normal")
        result = controller.execute_operation("factorial", [5])
        assert result["success"] is True
        assert result["result"] == 120

    def test_gui_controller_execute_operation_success_divide(self):
        """execute_operation('divide', [10, 2]) returns success dict with result 5.0."""
        controller = GUIController(mode="normal")
        result = controller.execute_operation("divide", [10, 2])
        assert result["success"] is True
        assert result["result"] == 5.0

    def test_gui_controller_execute_operation_divide_by_zero(self):
        """execute_operation('divide', [5, 0]) returns error dict (no result key)."""
        controller = GUIController(mode="normal")
        result = controller.execute_operation("divide", [5, 0])
        assert result["success"] is False
        assert "error" in result
        assert "result" not in result

    def test_gui_controller_execute_operation_domain_error_sqrt_negative(self):
        """execute_operation('square_root', [-1]) returns error dict."""
        controller = GUIController(mode="normal")
        result = controller.execute_operation("square_root", [-1])
        assert result["success"] is False
        assert "error" in result

    def test_gui_controller_execute_operation_unknown_operation(self):
        """execute_operation('nonexistent', [1, 2]) returns error with 'Unknown' or 'not found'."""
        controller = GUIController(mode="normal")
        result = controller.execute_operation("nonexistent", [1, 2])
        assert result["success"] is False
        assert "error" in result
        error_msg = result["error"].lower()
        assert "unknown" in error_msg or "not found" in error_msg

    def test_gui_controller_execute_operation_wrong_arity(self):
        """execute_operation('add', [5]) returns error about operands."""
        controller = GUIController(mode="normal")
        result = controller.execute_operation("add", [5])
        assert result["success"] is False
        assert "error" in result
        error_msg = result["error"].lower()
        assert "operand" in error_msg or "arity" in error_msg

    def test_gui_controller_execute_operation_not_available_in_mode(self):
        """Controller in normal mode, execute_operation('sin', [0]) returns error."""
        controller = GUIController(mode="normal")
        result = controller.execute_operation("sin", [0])
        assert result["success"] is False
        assert "error" in result
        error_msg = result["error"].lower()
        assert "not available" in error_msg


class TestGUIControllerOperationArity:
    """Test GUIController get_operation_arity() method."""

    def test_gui_controller_get_operation_arity_add(self):
        """get_operation_arity('add') returns 2."""
        controller = GUIController(mode="normal")
        arity = controller.get_operation_arity("add")
        assert arity == 2

    def test_gui_controller_get_operation_arity_factorial(self):
        """get_operation_arity('factorial') returns 1."""
        controller = GUIController(mode="normal")
        arity = controller.get_operation_arity("factorial")
        assert arity == 1

    def test_gui_controller_get_operation_arity_pi(self):
        """get_operation_arity('pi') returns 0."""
        controller = GUIController(mode="scientific")
        arity = controller.get_operation_arity("pi")
        assert arity == 0

    def test_gui_controller_get_operation_arity_unknown(self):
        """get_operation_arity('nonexistent') raises KeyError or returns None."""
        controller = GUIController(mode="normal")
        with pytest.raises(KeyError):
            controller.get_operation_arity("nonexistent")


class TestGUIControllerSessionHistory:
    """Test GUIController session history tracking."""

    def test_gui_controller_session_history_empty_at_init(self):
        """get_session_history() returns [] on fresh controller."""
        controller = GUIController(mode="normal")
        history = controller.get_session_history()
        assert history == []

    def test_gui_controller_session_history_recorded_after_operation(self):
        """Execute add([2,3]), get_session_history() returns list with 1 entry."""
        controller = GUIController(mode="normal")
        controller.execute_operation("add", [2, 3])
        history = controller.get_session_history()
        assert len(history) == 1

    def test_gui_controller_session_history_multiple_operations(self):
        """Execute 3 operations, get_session_history() returns list with 3 entries in order."""
        controller = GUIController(mode="normal")
        controller.execute_operation("add", [2, 3])
        controller.execute_operation("multiply", [4, 5])
        controller.execute_operation("divide", [10, 2])
        history = controller.get_session_history()
        assert len(history) == 3
        # Verify order: operations should appear in sequence
        assert "add" in history[0].lower() or "5" in str(history[0])
        assert "multiply" in history[1].lower() or "20" in str(history[1])
        assert "divide" in history[2].lower() or "5" in str(history[2])

    def test_gui_controller_session_history_not_recorded_on_error(self):
        """Execute divide([5, 0]) (error), get_session_history() returns []."""
        controller = GUIController(mode="normal")
        controller.execute_operation("divide", [5, 0])
        history = controller.get_session_history()
        assert history == []

    def test_gui_controller_clear_session_history(self):
        """Execute add([2,3]), clear_session_history(), get_session_history() returns []."""
        controller = GUIController(mode="normal")
        controller.execute_operation("add", [2, 3])
        assert len(controller.get_session_history()) == 1
        controller.clear_session_history()
        assert controller.get_session_history() == []
