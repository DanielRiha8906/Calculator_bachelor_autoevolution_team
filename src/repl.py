"""REPL interface for the Calculator.

Provides a Read-Eval-Print Loop allowing interactive use of all calculator
operations via a numbered menu driven command-line interface.
"""

from typing import TYPE_CHECKING, Optional

from src.exceptions import MaxRetriesExceeded
from src.error_logger import ErrorLogger
from src.operations import Operation, OperationRegistry, _CATALOG

if TYPE_CHECKING:
    from src.history import OperationHistory

MAX_RETRIES = 3

# Backwards-compatible module-level dict so that existing imports of the form
# ``from src.repl import OPERATIONS`` continue to work.  The dict is built
# from the canonical _CATALOG in src.operations so it stays in sync.
OPERATIONS: dict[str, dict] = {
    op.name: {"arity": op.arity, "name": op.display_name}
    for op in _CATALOG
}


class REPLInterface:
    """Interactive REPL for the Calculator.

    Presents a numbered menu of operations, collects operands from the user,
    invokes the corresponding Calculator method via
    :class:`~src.operations.OperationRegistry`, displays the result, and
    carries the result forward as a default for the next operation.

    Args:
        calculator: A Calculator instance whose methods will be called.
        history: An optional ``OperationHistory`` instance used to record each
            completed operation.  When ``None``, history recording and display
            are disabled.
        error_logger: An optional ``ErrorLogger`` instance used to record
            errors encountered during the session.  When ``None``, error
            logging is disabled.
    """

    def __init__(
        self,
        calculator,
        history: Optional["OperationHistory"] = None,
        error_logger: Optional[ErrorLogger] = None,
    ) -> None:
        self.calculator = calculator
        self.history = history
        self.error_logger = error_logger
        self.last_result: Optional[float] = None
        self._registry = OperationRegistry(calculator)
        # Ordered list of Operation objects — drives menu numbering.
        self._operations: list[Operation] = self._registry.get_operations()
        # Ordered list of canonical names — used for index-based selection.
        self._operation_keys: list[str] = [op.name for op in self._operations]

    def run(self) -> None:
        """Start the REPL loop.

        Repeatedly prompts for an operation, collects operands, executes the
        operation, and displays the result.  Exits cleanly when the user types
        "quit" or sends EOF.
        """
        print("Welcome to the Calculator REPL. Type 'quit' to exit.")
        while True:
            try:
                operation = self.get_operation_selection()
            except (EOFError, KeyboardInterrupt):
                print("\nCalculator closed.")
                return
            except MaxRetriesExceeded as exc:
                print(str(exc))
                return

            if operation == "quit":
                print("Calculator closed.")
                return

            if operation == "history":
                if self.history is not None:
                    entries = self.history.display_history()
                    if entries:
                        print("\nOperation history:")
                        for entry in entries:
                            print(f"  {entry}")
                    else:
                        print("No history recorded yet.")
                else:
                    print("History is not available in this session.")
                continue

            op_meta = self._registry.get_operation(operation)
            arity: int = op_meta.arity  # type: ignore[union-attr]
            operands: list[float] = []

            try:
                if arity == 1:
                    operand = self.get_operand(
                        self._first_operand_prompt("value")
                    )
                    operands.append(operand)
                else:
                    first = self.get_operand(
                        self._first_operand_prompt("first value")
                    )
                    operands.append(first)
                    self.last_result = None  # only offer carry-over for first operand
                    second = self.get_operand("Enter second value: ")
                    operands.append(second)
            except (EOFError, KeyboardInterrupt):
                print("\nCalculator closed.")
                return
            except MaxRetriesExceeded as exc:
                print(str(exc))
                return

            try:
                result = self._execute(operation, operands)
            except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
                print(f"Error: {exc}")
                if self.error_logger is not None:
                    operand_str = ", ".join(str(o) for o in operands)
                    user_input = f"{operation}({operand_str})"
                    self.error_logger.log_error(
                        ErrorLogger.CALCULATION_ERROR, user_input, exc
                    )
                continue

            self.display_result(operation, operands, result)
            self.last_result = result

            if self.history is not None:
                operand_str = ", ".join(str(o) for o in operands)
                entry = f"{operation}({operand_str}) = {result}"
                self.history.record_operation(entry)

    def _first_operand_prompt(self, label: str) -> str:
        """Build a prompt string that includes the last result if available.

        Args:
            label: Description of the operand (e.g. "value" or "first value").

        Returns:
            A formatted prompt string.
        """
        if self.last_result is not None:
            return f"Enter {label} [default: {self.last_result}]: "
        return f"Enter {label}: "

    def _execute(self, operation: str, operands: list[float]):
        """Dispatch an operation to the Calculator via the registry.

        Delegates to :meth:`~src.operations.OperationRegistry.dispatch`, which
        handles the special-case two-argument ``logarithm`` as well as all
        standard Calculator method calls.

        Args:
            operation: Canonical operation name (a key in the registry).
            operands: Collected operand values.

        Returns:
            The numeric result of the operation.

        Raises:
            ValueError: Propagated from calculator or math functions.
            ZeroDivisionError: Propagated from calculator.
            TypeError: Propagated from calculator (e.g. factorial of float).
            OverflowError: Propagated from math operations.
        """
        return self._registry.dispatch(operation, operands)

    def _is_valid_operand(self, raw_input: str) -> bool:
        """Return True if raw_input can be parsed as a float.

        Args:
            raw_input: The raw string supplied by the user.

        Returns:
            True when the stripped string is a valid float, False otherwise.
        """
        try:
            float(raw_input.strip())
            return True
        except ValueError:
            return False

    def _is_valid_operation_input(self, raw_input: str) -> bool:
        """Return True if raw_input is a valid operation selection or "quit".

        A valid selection is either the string "quit" (case-insensitive) or an
        integer in the range [1, len(_operation_keys)].

        Args:
            raw_input: The raw string supplied by the user.

        Returns:
            True when the input is "quit" or a valid menu index, False otherwise.
        """
        if raw_input.lower().strip() in ("quit", "history"):
            return True
        try:
            choice = int(raw_input.strip())
            return 1 <= choice <= len(self._operation_keys)
        except ValueError:
            return False

    def get_operation_selection(self) -> str:
        """Display the operation menu and return a validated operation key.

        Re-prompts until the user enters a valid menu number or "quit".  Raises
        MaxRetriesExceeded after MAX_RETRIES consecutive invalid inputs.

        Returns:
            A canonical operation name from the registry, or the string "quit".

        Raises:
            EOFError: If stdin is exhausted (propagated to caller).
            MaxRetriesExceeded: If the user provides invalid input MAX_RETRIES
                times in a row.
        """
        print("\nAvailable operations:")
        for idx, op in enumerate(self._operations, start=1):
            print(f"  {idx}. {op.display_name}")
        print("  history. Show operation history")
        print("  quit. Exit")

        attempts = 0
        while True:
            raw = input("Select operation: ").strip()
            if raw.lower() == "quit":
                return "quit"
            if raw.lower() == "history":
                return "history"
            try:
                choice = int(raw)
            except ValueError:
                attempts += 1
                if attempts >= MAX_RETRIES:
                    raise MaxRetriesExceeded(
                        "Maximum retry attempts exceeded. Session ended."
                    )
                print("Invalid selection. Enter a number from the list, 'history', or 'quit'.")
                continue
            if 1 <= choice <= len(self._operation_keys):
                return self._operation_keys[choice - 1]
            attempts += 1
            if attempts >= MAX_RETRIES:
                raise MaxRetriesExceeded(
                    "Maximum retry attempts exceeded. Session ended."
                )
            print(
                f"Invalid selection. Enter a number between 1 and "
                f"{len(self._operation_keys)}, 'history', or 'quit'."
            )

    def get_operand(self, prompt: str) -> float:
        """Prompt the user for a numeric value, re-prompting on invalid input.

        If self.last_result is set and the user presses Enter without typing a
        value, last_result is returned as the default.  Raises
        MaxRetriesExceeded after MAX_RETRIES consecutive invalid inputs.

        Args:
            prompt: The prompt string displayed to the user.

        Returns:
            A float value entered by the user (or the default last_result).

        Raises:
            EOFError: If stdin is exhausted (propagated to caller).
            MaxRetriesExceeded: If the user provides invalid input MAX_RETRIES
                times in a row.
        """
        attempts = 0
        while True:
            raw = input(prompt).strip()
            if raw == "" and self.last_result is not None:
                return float(self.last_result)
            try:
                return float(raw)
            except ValueError:
                attempts += 1
                if attempts >= MAX_RETRIES:
                    raise MaxRetriesExceeded(
                        "Maximum retry attempts exceeded. Session ended."
                    )
                print("Invalid number. Please enter a numeric value.")

    def display_result(self, operation: str, operands: list, result) -> None:
        """Print the result of an operation.

        Args:
            operation: Canonical operation name from the registry (e.g. "add").
            operands: The operand values used.
            result: The computed result.
        """
        op_meta = self._registry.get_operation(operation)
        op_name = op_meta.display_name  # type: ignore[union-attr]
        operand_str = ", ".join(str(o) for o in operands)
        print(f"{op_name}({operand_str}) = {result}")
