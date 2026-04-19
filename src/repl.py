"""REPL interface for the Calculator.

Provides a Read-Eval-Print Loop allowing interactive use of all calculator
operations via a numbered menu driven command-line interface.
"""

import math
from typing import Optional

from src.exceptions import MaxRetriesExceeded
from src.history import HistoryManager

MAX_RETRIES = 3

OPERATIONS: dict[str, dict] = {
    "add": {"arity": 2, "name": "Addition"},
    "subtract": {"arity": 2, "name": "Subtraction"},
    "multiply": {"arity": 2, "name": "Multiplication"},
    "divide": {"arity": 2, "name": "Division"},
    "power": {"arity": 2, "name": "Power"},
    "logarithm": {"arity": 2, "name": "Logarithm (base)"},
    "factorial": {"arity": 1, "name": "Factorial"},
    "square": {"arity": 1, "name": "Square"},
    "cube": {"arity": 1, "name": "Cube"},
    "square_root": {"arity": 1, "name": "Square Root"},
    "cube_root": {"arity": 1, "name": "Cube Root"},
    "natural_logarithm": {"arity": 1, "name": "Natural Logarithm"},
}

_OPERATION_KEYS: list[str] = list(OPERATIONS.keys())


class REPLInterface:
    """Interactive REPL for the Calculator.

    Presents a numbered menu of operations, collects operands from the user,
    invokes the corresponding Calculator method, displays the result, and
    carries the result forward as a default for the next operation.

    Args:
        calculator: A Calculator instance whose methods will be called.
    """

    def __init__(self, calculator) -> None:
        self.calculator = calculator
        self.last_result: Optional[float] = None
        self.history_manager = HistoryManager()

    def run(self) -> None:
        """Start the REPL loop.

        Repeatedly prompts for an operation, collects operands, executes the
        operation, and displays the result.  Exits cleanly when the user types
        "quit" or sends EOF.
        """
        print("Welcome to the Calculator REPL. Type 'quit' to exit.")
        self.history_manager.clear()
        while True:
            try:
                operation = self.get_operation_selection()
            except (EOFError, KeyboardInterrupt):
                print("\nCalculator closed.")
                return
            except MaxRetriesExceeded as exc:
                print(str(exc))
                return

            if operation == "history":
                self.display_history()
                continue

            if operation == "quit":
                print("Calculator closed.")
                return

            meta = OPERATIONS[operation]
            arity: int = meta["arity"]
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
                continue

            self.display_result(operation, operands, result)
            self.history_manager.record_operation(operation, operands, result)
            self.last_result = result

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
        """Dispatch an operation to the Calculator or built-in math.

        The "logarithm" operation is treated as a two-argument logarithm
        (log(x, base)) because Calculator.logarithm only accepts one argument
        (base-10).  All other operations are dispatched via getattr.

        Args:
            operation: Key from OPERATIONS.
            operands: Collected operand values.

        Returns:
            The numeric result of the operation.

        Raises:
            ValueError: Propagated from calculator or math functions.
            ZeroDivisionError: Propagated from calculator.
            TypeError: Propagated from calculator (e.g. factorial of float).
            OverflowError: Propagated from math operations.
        """
        if operation == "logarithm":
            x, base = operands
            if base <= 0 or base == 1:
                raise ValueError(
                    "logarithm base must be positive and not equal to 1"
                )
            if x <= 0:
                raise ValueError(
                    "logarithm() not defined for non-positive values"
                )
            return math.log(x, base)

        method = getattr(self.calculator, operation)
        return method(*operands)

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
        integer in the range [1, len(_OPERATION_KEYS)].

        Args:
            raw_input: The raw string supplied by the user.

        Returns:
            True when the input is "quit" or a valid menu index, False otherwise.
        """
        if raw_input.lower().strip() in ("quit", "history"):
            return True
        try:
            choice = int(raw_input.strip())
            return 1 <= choice <= len(_OPERATION_KEYS)
        except ValueError:
            return False

    def get_operation_selection(self) -> str:
        """Display the operation menu and return a validated operation key.

        Re-prompts until the user enters a valid menu number or "quit".  Raises
        MaxRetriesExceeded after MAX_RETRIES consecutive invalid inputs.

        Returns:
            A key from OPERATIONS, or the string "quit".

        Raises:
            EOFError: If stdin is exhausted (propagated to caller).
            MaxRetriesExceeded: If the user provides invalid input MAX_RETRIES
                times in a row.
        """
        print("\nAvailable operations:")
        for idx, key in enumerate(_OPERATION_KEYS, start=1):
            print(f"  {idx}. {OPERATIONS[key]['name']}")
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
                print("Invalid selection. Enter a number from the list or 'quit'.")
                continue
            if 1 <= choice <= len(_OPERATION_KEYS):
                return _OPERATION_KEYS[choice - 1]
            attempts += 1
            if attempts >= MAX_RETRIES:
                raise MaxRetriesExceeded(
                    "Maximum retry attempts exceeded. Session ended."
                )
            print(
                f"Invalid selection. Enter a number between 1 and "
                f"{len(_OPERATION_KEYS)}, or 'quit'."
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
            operation: Key from OPERATIONS (e.g. "add").
            operands: The operand values used.
            result: The computed result.
        """
        op_name = OPERATIONS[operation]["name"]
        operand_str = ", ".join(str(o) for o in operands)
        print(f"{op_name}({operand_str}) = {result}")

    def display_history(self) -> None:
        """Print all recorded operations for the current session.

        Retrieves the history entries from the HistoryManager and prints each
        entry on a separate line.  If no operations have been recorded yet,
        prints an informational message instead.
        """
        entries = self.history_manager.get_history()
        if not entries:
            print("No operations recorded yet.")
        else:
            print("Operation History:")
            for entry in entries:
                print(entry)
