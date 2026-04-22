"""Encapsulates all user input and output operations for the calculator."""


class InputHandler:
    """Handles user-facing input prompts and output display."""

    def get_operation_choice(self, available_operations: dict) -> str:
        """Display the operation list, prompt the user, and return a valid selection.

        Re-prompts on invalid input. Accepts "exit" or "quit" as special
        sentinel values, which are returned directly without validation
        against ``available_operations``.

        Args:
            available_operations: Mapping of operation key -> display string.

        Returns:
            A key present in ``available_operations``, or "exit" / "quit".
        """
        print("\nAvailable operations:")
        for key, description in available_operations.items():
            print(f"  {key}: {description}")
        print("  exit / quit: Exit the calculator")

        while True:
            choice = input("Select an operation: ").strip().lower()
            if choice in ("exit", "quit"):
                return choice
            if choice in available_operations:
                return choice
            print(f"Invalid choice '{choice}'. Please select from the list above.")

    def get_operand(self, prompt: str) -> float:
        """Prompt the user for a numeric value and return it as a float.

        Args:
            prompt: The message shown to the user.

        Returns:
            The parsed float value.

        Raises:
            ValueError: If the input cannot be converted to a float.
        """
        raw = input(prompt).strip()
        return float(raw)

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
