"""Encapsulates all user input and output operations for the calculator."""

from typing import Any

from .validation import validate_operand, get_validation_error_message

MAX_RETRIES: int = 3


class InputRetryExhaustedError(ValueError):
    """Raised when the user exhausts all retry attempts for an input prompt."""


class InputHandler:
    """Handles user-facing input prompts and output display."""

    def __init__(self, history: Any = None) -> None:
        """Initialise the handler, optionally attaching an operation history store.

        Args:
            history: An :class:`~history.OperationHistory` instance (or any object
                exposing a ``display_history() -> str`` method), or ``None`` if
                history tracking is not required.
        """
        self.history: Any = history

    def display_history(self) -> None:
        """Print the current operation history to stdout.

        Delegates to ``self.history.display_history()`` when a history store is
        attached; otherwise prints a generic unavailable message.
        """
        if self.history is not None:
            print(self.history.display_history())
        else:
            print("No history available.")

    def get_operation_choice(
        self,
        available_operations: dict,
        max_retries: int = MAX_RETRIES,
    ) -> str:
        """Display the operation list, prompt the user, and return a valid selection.

        Accepts "exit" or "quit" as special sentinel values, which are returned
        directly without validation against ``available_operations`` and without
        counting as a failed attempt.  Accepts "history" as a display-only
        sentinel: the operation history is printed and the user is re-prompted
        without consuming a retry attempt and without returning to the caller.

        After ``max_retries`` consecutive invalid choices, prints a session-ended
        message and raises ``InputRetryExhaustedError``.

        Args:
            available_operations: Mapping of operation key -> display string.
            max_retries: Maximum number of invalid attempts before aborting.

        Returns:
            A key present in ``available_operations``, or "exit" / "quit".

        Raises:
            InputRetryExhaustedError: When ``max_retries`` invalid entries are
                made in succession.
        """
        print("\nAvailable operations:")
        for key, description in available_operations.items():
            print(f"  {key}: {description}")
        print("  exit / quit: Exit the calculator")

        retries: int = 0
        while retries < max_retries:
            choice = input("Select an operation: ").strip().lower()
            if choice in ("exit", "quit"):
                return choice
            if choice == "history":
                self.display_history()
                continue
            if choice in available_operations:
                return choice
            retries += 1
            remaining = max_retries - retries
            print(
                f"Invalid choice '{choice}'. Please select from the list above."
                + (f" ({remaining} attempt(s) remaining)" if remaining > 0 else "")
            )

        print("Maximum retry attempts reached. Session ended.")
        raise InputRetryExhaustedError(
            "User exhausted all retry attempts for operation selection."
        )

    def get_operand(self, prompt: str, max_retries: int = MAX_RETRIES) -> float:
        """Prompt the user for a numeric value and return it as a float.

        On invalid input, displays an error message and re-prompts up to
        ``max_retries`` times.  After all attempts are exhausted, prints a
        session-ended message and raises ``InputRetryExhaustedError``.

        Args:
            prompt: The message shown to the user.
            max_retries: Maximum number of invalid attempts before aborting.

        Returns:
            The parsed float value.

        Raises:
            InputRetryExhaustedError: When ``max_retries`` invalid entries are
                made in succession.
        """
        retries: int = 0
        while retries < max_retries:
            raw = input(prompt).strip()
            try:
                return validate_operand(raw)
            except Exception as exc:
                retries += 1
                remaining = max_retries - retries
                detail = get_validation_error_message(exc)
                print(
                    f"Error: Invalid operand — {detail}. Please try again."
                    + (f" ({remaining} attempt(s) remaining)" if remaining > 0 else "")
                )

        print("Maximum retry attempts reached. Session ended.")
        raise InputRetryExhaustedError(
            "User exhausted all retry attempts for operand input."
        )

    def display_result(self, operation: str, operands: list, result: float) -> None:
        """Format and print the operation result.

        Args:
            operation: Human-readable name of the operation performed.
            operands: List of operand values used in the operation.
            result: The computed result.
        """
        operands_str = ", ".join(str(o) for o in operands)
        print(f"Result of {operation}({operands_str}) = {result}")

    def display_error(self, message: str) -> None:
        """Print a user-friendly error message.

        Args:
            message: The error description to display.
        """
        print(f"Error: {message}")


class UserInterface:
    """Handles all display and presentation output for the calculator.

    This class is pure output only — it contains no input-prompting logic.
    All methods write to stdout and return ``None``.
    """

    def display_result(self, operation: str, operands: list, result: float) -> None:
        """Format and print the operation result.

        Args:
            operation: Human-readable name of the operation performed.
            operands: List of operand values used in the operation.
            result: The computed result.
        """
        operands_str = ", ".join(str(o) for o in operands)
        print(f"Result of {operation}({operands_str}) = {result}")

    def display_error(self, message: str) -> None:
        """Print a user-friendly error message.

        Args:
            message: The error description to display.
        """
        print(f"Error: {message}")

    def display_operations(self, available_operations: dict) -> None:
        """Print the list of available operations.

        Args:
            available_operations: Mapping of operation key to display string.
        """
        print("\nAvailable operations:")
        for key, description in available_operations.items():
            print(f"  {key}: {description}")
        print("  exit / quit: Exit the calculator")

    def display_history(self, history_str: str) -> None:
        """Print the provided history string.

        Args:
            history_str: A pre-formatted, human-readable history string as
                returned by :meth:`~history.OperationHistory.display_history`.
        """
        print(history_str)
