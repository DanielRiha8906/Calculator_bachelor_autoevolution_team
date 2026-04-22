"""User interaction orchestration and session flow management."""

from .engine import CalculationEngine
from .history import OperationHistory
from .io_handler import InputHandler, UserInterface


class CalculatorWorkflow:
    """Manages the calculator session loop.

    Coordinates between the input handler, UI, calculation engine, and
    operation history to drive the full user-facing calculator experience.
    The class contains no arithmetic logic itself — computation is fully
    delegated to :class:`~engine.CalculationEngine`.
    """

    def __init__(
        self,
        engine: CalculationEngine,
        input_handler: InputHandler,
        ui: UserInterface,
        history: OperationHistory,
    ) -> None:
        """Initialise the workflow with all required collaborators.

        Args:
            engine: The calculation engine responsible for executing operations.
            input_handler: Handles all user input prompts.
            ui: Handles all display and presentation output.
            history: Persists and retrieves the operation history.
        """
        self._engine: CalculationEngine = engine
        self._input_handler: InputHandler = input_handler
        self._ui: UserInterface = ui
        self._history: OperationHistory = history

    def run(self) -> None:
        """Run the main calculator session loop.

        Prompts the user to select an operation, collects the required
        operands, executes the calculation, records it in the history, and
        displays the result.  The loop continues until the user enters
        ``"exit"`` or ``"quit"``, or until the input handler exhausts all
        retry attempts.
        """
        available_operations = self._engine._registry.list_operations()

        while True:
            operation_key = self._input_handler.get_operation_choice(
                available_operations
            )

            if operation_key in ("exit", "quit"):
                break

            try:
                operands = self._get_operands(operation_key)
            except Exception as exc:
                self._handle_calculation_error(exc)
                continue

            try:
                result = self._engine.execute_operation(operation_key, operands)
            except Exception as exc:
                self._handle_calculation_error(exc)
                continue

            self._history.record_operation(operation_key, operands, result)
            self._ui.display_result(operation_key, operands, result)

    def _get_operands(self, operation_key: str) -> list[float]:
        """Collect the operands required for the given operation.

        Determines the arity of the operation from the registry and prompts
        the user once for each required operand.

        Args:
            operation_key: The string identifier of the chosen operation.

        Returns:
            A list of float operand values with length equal to the operation
            arity.

        Raises:
            InputRetryExhaustedError: If the user exhausts retry attempts for
                any operand prompt.
        """
        _method, arity, _description = self._engine._registry.get_operation(
            operation_key
        )

        operands: list[float] = []
        if arity == 1:
            operands.append(
                self._input_handler.get_operand(f"Enter operand for {operation_key}: ")
            )
        else:
            for index in range(1, arity + 1):
                operands.append(
                    self._input_handler.get_operand(
                        f"Enter operand {index} for {operation_key}: "
                    )
                )
        return operands

    def _handle_calculation_error(self, error: Exception) -> None:
        """Display a user-friendly error message for a caught exception.

        Args:
            error: The exception raised during operand collection or
                operation execution.
        """
        self._ui.display_error(str(error))
