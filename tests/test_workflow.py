"""Comprehensive tests for CalculatorWorkflow."""

import pytest
from unittest.mock import Mock, MagicMock, call, patch
from src.workflow import CalculatorWorkflow
from src.engine import CalculationEngine
from src.io_handler import InputHandler, UserInterface, InputRetryExhaustedError
from src.calculator import Calculator
from src.operations import OperationRegistry
from src.history import OperationHistory


class TestWorkflowInitialization:
    """Test suite for CalculatorWorkflow initialization."""

    def test_workflow_initializes_with_all_dependencies(self):
        """Test that workflow initializes correctly with all required collaborators."""
        engine = Mock(spec=CalculationEngine)
        input_handler = Mock(spec=InputHandler)
        ui = Mock(spec=UserInterface)
        history = Mock(spec=OperationHistory)

        workflow = CalculatorWorkflow(engine, input_handler, ui, history)

        assert workflow._engine is engine
        assert workflow._input_handler is input_handler
        assert workflow._ui is ui
        assert workflow._history is history

    def test_workflow_with_real_dependencies(self):
        """Test workflow initialization with real object instances."""
        calculator = Calculator()
        registry = OperationRegistry(calculator)
        engine = CalculationEngine(calculator, registry)
        input_handler = InputHandler()
        ui = UserInterface()
        history = OperationHistory()

        workflow = CalculatorWorkflow(engine, input_handler, ui, history)

        assert workflow._engine is engine
        assert workflow._input_handler is input_handler
        assert workflow._ui is ui
        assert workflow._history is history


class TestWorkflowGetOperands:
    """Test suite for CalculatorWorkflow._get_operands()."""

    @pytest.fixture
    def workflow(self):
        """Fixture providing a CalculatorWorkflow with real dependencies."""
        calculator = Calculator()
        registry = OperationRegistry(calculator)
        engine = CalculationEngine(calculator, registry)
        input_handler = InputHandler()
        ui = UserInterface()
        history = OperationHistory()
        return CalculatorWorkflow(engine, input_handler, ui, history)

    @patch.object(InputHandler, 'get_operand', return_value=5.0)
    def test_get_operands_unary_operation(self, mock_get_operand, workflow):
        """Test that _get_operands returns single element list for unary operations."""
        operands = workflow._get_operands("square")
        assert operands == [5.0]
        assert len(operands) == 1
        assert mock_get_operand.call_count == 1

    @patch.object(InputHandler, 'get_operand', side_effect=[3.0, 4.0])
    def test_get_operands_binary_operation(self, mock_get_operand, workflow):
        """Test that _get_operands returns two element list for binary operations."""
        operands = workflow._get_operands("add")
        assert operands == [3.0, 4.0]
        assert len(operands) == 2
        assert mock_get_operand.call_count == 2

    @patch.object(InputHandler, 'get_operand', side_effect=[10.0, 2.0])
    def test_get_operands_binary_divide(self, mock_get_operand, workflow):
        """Test _get_operands for divide operation."""
        operands = workflow._get_operands("divide")
        assert operands == [10.0, 2.0]
        assert len(operands) == 2

    @patch.object(InputHandler, 'get_operand', return_value=9.0)
    def test_get_operands_square_root_is_unary(self, mock_get_operand, workflow):
        """Test that square_root (unary) collects one operand."""
        operands = workflow._get_operands("square_root")
        assert operands == [9.0]
        assert len(operands) == 1

    @patch.object(InputHandler, 'get_operand', return_value=5.0)
    def test_get_operands_factorial_is_unary(self, mock_get_operand, workflow):
        """Test that factorial (unary) collects one operand."""
        operands = workflow._get_operands("factorial")
        assert operands == [5.0]
        assert len(operands) == 1

    @patch.object(InputHandler, 'get_operand', side_effect=[2.0, 8.0])
    def test_get_operands_power_is_binary(self, mock_get_operand, workflow):
        """Test that power (binary) collects two operands."""
        operands = workflow._get_operands("power")
        assert operands == [2.0, 8.0]
        assert len(operands) == 2

    @patch.object(InputHandler, 'get_operand', side_effect=InputRetryExhaustedError("Max retries"))
    def test_get_operands_propagates_input_retry_exhausted_error(self, mock_get_operand, workflow):
        """Test that _get_operands propagates InputRetryExhaustedError."""
        with pytest.raises(InputRetryExhaustedError):
            workflow._get_operands("add")

    @patch.object(InputHandler, 'get_operand', side_effect=[5.0, InputRetryExhaustedError("Max retries")])
    def test_get_operands_error_on_second_operand_propagates(self, mock_get_operand, workflow):
        """Test that error on second operand collection propagates."""
        with pytest.raises(InputRetryExhaustedError):
            workflow._get_operands("add")


class TestWorkflowHandleCalculationError:
    """Test suite for CalculatorWorkflow._handle_calculation_error()."""

    @pytest.fixture
    def workflow(self):
        """Fixture providing a CalculatorWorkflow."""
        engine = Mock(spec=CalculationEngine)
        input_handler = Mock(spec=InputHandler)
        ui = Mock(spec=UserInterface)
        history = Mock(spec=OperationHistory)
        return CalculatorWorkflow(engine, input_handler, ui, history)

    def test_handle_calculation_error_displays_error(self, workflow):
        """Test that _handle_calculation_error calls ui.display_error()."""
        error = ValueError("Test error message")
        workflow._handle_calculation_error(error)
        workflow._ui.display_error.assert_called_once_with("Test error message")

    def test_handle_calculation_error_with_zero_division_error(self, workflow):
        """Test that ZeroDivisionError is displayed correctly."""
        error = ZeroDivisionError("division by zero")
        workflow._handle_calculation_error(error)
        workflow._ui.display_error.assert_called_once_with("division by zero")

    def test_handle_calculation_error_with_custom_message(self, workflow):
        """Test that custom error messages are preserved."""
        error = ValueError("Square root is not defined for negative numbers")
        workflow._handle_calculation_error(error)
        workflow._ui.display_error.assert_called_once_with(
            "Square root is not defined for negative numbers"
        )

    def test_handle_calculation_error_with_generic_exception(self, workflow):
        """Test that generic exceptions are handled."""
        error = Exception("Generic error")
        workflow._handle_calculation_error(error)
        workflow._ui.display_error.assert_called_once_with("Generic error")


class TestWorkflowSessionFlow:
    """Test suite for CalculatorWorkflow.run() session flow."""

    @pytest.fixture
    def workflow(self):
        """Fixture providing a CalculatorWorkflow with mocked dependencies."""
        engine = Mock(spec=CalculationEngine)
        input_handler = Mock(spec=InputHandler)
        ui = Mock(spec=UserInterface)
        history = Mock(spec=OperationHistory)

        # Mock the registry's list_operations
        mock_registry = Mock(spec=OperationRegistry)
        mock_registry.list_operations.return_value = {
            "add": "Addition",
            "subtract": "Subtraction",
        }
        engine._registry = mock_registry

        return CalculatorWorkflow(engine, input_handler, ui, history)

    def test_run_exits_on_exit_sentinel(self, workflow):
        """Test that run() exits immediately when 'exit' is selected."""
        workflow._input_handler.get_operation_choice.return_value = "exit"

        workflow.run()

        # Verify that we didn't try to get operands or execute
        workflow._input_handler.get_operand.assert_not_called()
        workflow._engine.execute_operation.assert_not_called()

    def test_run_exits_on_quit_sentinel(self, workflow):
        """Test that run() exits immediately when 'quit' is selected."""
        workflow._input_handler.get_operation_choice.return_value = "quit"

        workflow.run()

        # Verify that we didn't try to get operands or execute
        workflow._input_handler.get_operand.assert_not_called()
        workflow._engine.execute_operation.assert_not_called()

    def test_run_successful_operation_cycle(self, workflow):
        """Test a successful operation cycle: select -> collect operands -> execute -> record -> display."""
        # Setup
        workflow._input_handler.get_operation_choice.side_effect = ["add", "exit"]
        # Mock _get_operands to return operands
        workflow._get_operands = Mock(return_value=[3.0, 4.0])
        workflow._engine.execute_operation.return_value = 7.0

        # Execute
        workflow.run()

        # Verify the full cycle
        assert workflow._input_handler.get_operation_choice.call_count == 2  # "add", then "exit"
        workflow._get_operands.assert_called_once_with("add")
        workflow._engine.execute_operation.assert_called_once_with("add", [3.0, 4.0])
        workflow._history.record_operation.assert_called_once_with("add", [3.0, 4.0], 7.0)
        workflow._ui.display_result.assert_called_once_with("add", [3.0, 4.0], 7.0)

    def test_run_multiple_successful_operations(self, workflow):
        """Test multiple successful operations in a session."""
        workflow._input_handler.get_operation_choice.side_effect = ["add", "subtract", "exit"]
        workflow._get_operands = Mock(side_effect=[[3.0, 4.0], [10.0, 2.0]])
        workflow._engine.execute_operation.side_effect = [7.0, 8.0]

        workflow.run()

        # Verify multiple cycles
        assert workflow._input_handler.get_operation_choice.call_count == 3
        assert workflow._get_operands.call_count == 2
        assert workflow._engine.execute_operation.call_count == 2
        assert workflow._history.record_operation.call_count == 2
        assert workflow._ui.display_result.call_count == 2

    def test_run_handles_value_error_on_operand_collection(self, workflow):
        """Test that ValueError during operand collection is handled gracefully."""
        workflow._input_handler.get_operation_choice.side_effect = ["add", "exit"]
        workflow._input_handler.get_operand.side_effect = ValueError("Invalid operand")

        workflow.run()

        # Verify error was handled
        workflow._ui.display_error.assert_called_once()
        # Verify we didn't try to execute
        workflow._engine.execute_operation.assert_not_called()

    def test_run_handles_value_error_on_execution(self, workflow):
        """Test that ValueError during execution is handled gracefully."""
        workflow._input_handler.get_operation_choice.side_effect = ["square_root", "exit"]
        workflow._input_handler.get_operand.side_effect = [-1.0]
        workflow._engine.execute_operation.side_effect = ValueError(
            "Square root is not defined for negative numbers"
        )

        workflow.run()

        # Verify error was handled
        workflow._ui.display_error.assert_called_once()
        # Verify history was not recorded
        workflow._history.record_operation.assert_not_called()
        # Verify result was not displayed
        workflow._ui.display_result.assert_not_called()

    def test_run_handles_zero_division_error(self, workflow):
        """Test that ZeroDivisionError during execution is handled gracefully."""
        workflow._input_handler.get_operation_choice.side_effect = ["divide", "exit"]
        workflow._input_handler.get_operand.side_effect = [5.0, 0.0]
        workflow._engine.execute_operation.side_effect = ZeroDivisionError("division by zero")

        workflow.run()

        # Verify error was handled
        workflow._ui.display_error.assert_called_once()
        # Verify history was not recorded
        workflow._history.record_operation.assert_not_called()

    def test_run_ends_on_input_retry_exhausted_error_during_operand_collection(self, workflow):
        """Test that InputRetryExhaustedError during operand collection ends session."""
        # First "add" triggers error in _get_operands, then "exit" to end session
        workflow._input_handler.get_operation_choice.side_effect = ["add", "exit"]
        workflow._get_operands = Mock(side_effect=InputRetryExhaustedError("Max retries exhausted"))

        workflow.run()

        # Verify error was handled
        workflow._ui.display_error.assert_called_once()
        # Operation choice was called twice (add, then exit)
        assert workflow._input_handler.get_operation_choice.call_count == 2

    def test_run_continues_after_error_until_exit(self, workflow):
        """Test that session continues after an error until exit is selected."""
        workflow._input_handler.get_operation_choice.side_effect = ["add", "add", "exit"]
        # First call raises error, second call succeeds
        workflow._get_operands = Mock(side_effect=[ValueError("First error"), [3.0, 4.0]])
        workflow._engine.execute_operation.return_value = 7.0

        workflow.run()

        # First operation fails (error handled), second succeeds, then exit
        assert workflow._input_handler.get_operation_choice.call_count == 3
        assert workflow._engine.execute_operation.call_count == 1  # Only second attempt
        assert workflow._history.record_operation.call_count == 1  # Only second attempt


class TestWorkflowIntegration:
    """Integration tests for CalculatorWorkflow with real dependencies."""

    def test_workflow_with_real_dependencies_successful_operation(self, tmp_path):
        """Test workflow with real dependencies for a successful operation."""
        calculator = Calculator()
        registry = OperationRegistry(calculator)
        engine = CalculationEngine(calculator, registry)
        input_handler = InputHandler()
        ui = UserInterface()
        history_file = tmp_path / "history.txt"
        history = OperationHistory(str(history_file))

        workflow = CalculatorWorkflow(engine, input_handler, ui, history)

        # Mock input to avoid actual user input
        with patch.object(input_handler, 'get_operation_choice', side_effect=["add", "exit"]):
            with patch.object(input_handler, 'get_operand', side_effect=[5.0, 3.0]):
                with patch.object(ui, 'display_result') as mock_display:
                    workflow.run()

                    # Verify the operation was recorded
                    mock_display.assert_called_once_with("add", [5.0, 3.0], 8.0)

        # Verify history was actually recorded
        history_text = history.display_history()
        assert "add(5.0, 3.0) = 8.0" in history_text

    def test_workflow_with_real_dependencies_division_by_zero(self, tmp_path):
        """Test workflow handles division by zero error."""
        calculator = Calculator()
        registry = OperationRegistry(calculator)
        engine = CalculationEngine(calculator, registry)
        input_handler = InputHandler()
        ui = UserInterface()
        history_file = tmp_path / "history.txt"
        history = OperationHistory(str(history_file))

        workflow = CalculatorWorkflow(engine, input_handler, ui, history)

        with patch.object(input_handler, 'get_operation_choice', side_effect=["divide", "exit"]):
            with patch.object(input_handler, 'get_operand', side_effect=[5.0, 0.0]):
                with patch.object(ui, 'display_error') as mock_error:
                    workflow.run()

                    # Verify error was displayed
                    mock_error.assert_called_once()
                    assert "division by zero" in str(mock_error.call_args).lower() or \
                           "zero" in str(mock_error.call_args).lower()

        # Verify history was NOT recorded
        history_text = history.display_history()
        assert "No history yet." in history_text


class TestWorkflowEdgeCases:
    """Edge case tests for CalculatorWorkflow."""

    @pytest.fixture
    def workflow(self):
        """Fixture providing a CalculatorWorkflow with mocked dependencies."""
        engine = Mock(spec=CalculationEngine)
        input_handler = Mock(spec=InputHandler)
        ui = Mock(spec=UserInterface)
        history = Mock(spec=OperationHistory)

        mock_registry = Mock(spec=OperationRegistry)
        mock_registry.list_operations.return_value = {"add": "Addition"}
        engine._registry = mock_registry

        return CalculatorWorkflow(engine, input_handler, ui, history)

    def test_run_with_large_operands(self, workflow):
        """Test that workflow can handle very large operand values."""
        workflow._input_handler.get_operation_choice.side_effect = ["add", "exit"]
        workflow._get_operands = Mock(return_value=[1e100, 2e100])
        workflow._engine.execute_operation.return_value = 3e100

        workflow.run()

        workflow._engine.execute_operation.assert_called_once_with("add", [1e100, 2e100])
        workflow._history.record_operation.assert_called_once_with("add", [1e100, 2e100], 3e100)

    def test_run_with_very_small_operands(self, workflow):
        """Test that workflow can handle very small operand values."""
        workflow._input_handler.get_operation_choice.side_effect = ["add", "exit"]
        workflow._get_operands = Mock(return_value=[1e-100, 2e-100])
        workflow._engine.execute_operation.return_value = 3e-100

        workflow.run()

        workflow._engine.execute_operation.assert_called_once_with("add", [1e-100, 2e-100])

    def test_run_with_negative_operands(self, workflow):
        """Test that workflow correctly handles negative operands."""
        workflow._input_handler.get_operation_choice.side_effect = ["subtract", "exit"]
        workflow._get_operands = Mock(return_value=[-5.0, -3.0])
        workflow._engine.execute_operation.return_value = -2.0

        workflow.run()

        workflow._engine.execute_operation.assert_called_once_with("subtract", [-5.0, -3.0])
