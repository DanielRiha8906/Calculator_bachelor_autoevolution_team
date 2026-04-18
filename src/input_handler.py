"""Interactive session loop for the Calculator application.

This module provides an operation registry, an InputHandler class that drives a
REPL-style session, and a convenience function for bootstrapping the session
from an external entry point.
"""

from __future__ import annotations

from typing import Callable

from .calculator import Calculator
from .history import History


# Maximum number of consecutive invalid inputs before the session is terminated.
MAX_RETRIES: int = 5

# Operations registry: insertion order defines menu display order.
# Each entry maps a user-facing key to metadata needed to dispatch the call.
OPERATIONS: dict[str, dict] = {
    "add": {
        "method": "add",
        "arity": 2,
        "label": "Add two numbers",
    },
    "subtract": {
        "method": "subtract",
        "arity": 2,
        "label": "Subtract two numbers",
    },
    "multiply": {
        "method": "multiply",
        "arity": 2,
        "label": "Multiply two numbers",
    },
    "divide": {
        "method": "divide",
        "arity": 2,
        "label": "Divide two numbers",
    },
    "power": {
        "method": "power",
        "arity": 2,
        "label": "Raise a number to a power",
    },
    "factorial": {
        "method": "factorial",
        "arity": 1,
        "label": "Factorial of a non-negative integer",
        "coerce": int,
    },
    "square": {
        "method": "square",
        "arity": 1,
        "label": "Square a number (x^2)",
    },
    "cube": {
        "method": "cube",
        "arity": 1,
        "label": "Cube a number (x^3)",
    },
    "square_root": {
        "method": "square_root",
        "arity": 1,
        "label": "Square root of a number",
    },
    "cube_root": {
        "method": "cube_root",
        "arity": 1,
        "label": "Cube root of a number",
    },
    "log10": {
        "method": "log10",
        "arity": 1,
        "label": "Base-10 logarithm of a number",
    },
    "ln": {
        "method": "ln",
        "arity": 1,
        "label": "Natural logarithm of a number",
    },
}


class InputHandler:
    """Drives an interactive calculator session.

    Args:
        calculator: A Calculator instance to which operations are dispatched.
        input_fn: Callable used to read user input; defaults to the built-in
            ``input``. Inject a custom callable in tests to avoid touching
            ``builtins.input``.
    """

    def __init__(
        self,
        calculator: Calculator,
        input_fn: Callable[[str], str] | None = None,
    ) -> None:
        self._calculator = calculator
        self._input_fn: Callable[[str], str] = input_fn if input_fn is not None else input
        self._history = History()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Run the interactive session loop.

        Prints the operation menu, reads the user's choice, collects operands,
        dispatches to the Calculator, and prints the result.  The loop exits
        when the user enters "exit" or "quit" at the operation prompt, or when
        the number of consecutive invalid operation inputs reaches MAX_RETRIES.
        Catches ValueError, ZeroDivisionError, and TypeError, printing a
        user-friendly message without crashing.
        """
        op_attempts: int = 0
        try:
            while True:
                self._show_menu()
                try:
                    op_choice = self._input_fn("Enter operation (or 'exit'/'quit' to stop): ").strip().lower()
                except StopIteration:
                    print("Goodbye!")
                    break

                if op_choice in ("exit", "quit"):
                    print("Goodbye!")
                    break

                if op_choice == "history":
                    entries = self._history.get_all()
                    if entries:
                        print("\n".join(entries))
                    else:
                        print("No history yet.")
                    continue

                if op_choice not in OPERATIONS:
                    op_attempts += 1
                    print(f"Error: Unknown operation '{op_choice}'. Please choose from the menu.")
                    print("Available operations: " + ", ".join(OPERATIONS.keys()))
                    if op_attempts >= MAX_RETRIES:
                        print("Too many invalid attempts. Ending session.")
                        break
                    continue

                op_attempts = 0
                op_info = OPERATIONS[op_choice]
                arity: int = op_info["arity"]
                coerce: Callable = op_info.get("coerce", float)  # type: ignore[assignment]

                try:
                    operands = self._prompt_operands(arity, coerce)
                except StopIteration:
                    print("Goodbye!")
                    break
                except ValueError as exc:
                    print(f"Error: {exc}")
                    continue

                try:
                    result = self._dispatch(op_choice, operands)
                except ZeroDivisionError:
                    print("Error: Division by zero is not allowed.")
                    continue
                except ValueError as exc:
                    print(f"Error: {exc}")
                    continue
                except TypeError as exc:
                    print(f"Error: {exc}")
                    continue

                print(f"Result: {result}")
                self._history.add_operation(op_choice, operands, result)
        finally:
            try:
                self._history.save_to_file("history.txt")
            except OSError as exc:
                print(f"Warning: Could not save history to file: {exc}")

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _show_menu(self) -> None:
        """Print the list of available operations to stdout."""
        print("\nAvailable operations:")
        for key, info in OPERATIONS.items():
            print(f"  {key:<14} — {info['label']}")

    def _prompt_operands(self, arity: int, coerce: Callable = float) -> list:
        """Prompt the user for the required number of operands.

        For each operand position, up to MAX_RETRIES attempts are made.  On
        each failed coerce attempt the error is printed and the same operand is
        re-prompted.  After MAX_RETRIES consecutive failures for a single
        operand a ValueError is raised to abort the current operation.

        Args:
            arity: Number of operands to collect (1 or 2).
            coerce: Callable used to convert the raw string to a numeric value;
                defaults to ``float``.

        Returns:
            A list of converted operand values.

        Raises:
            ValueError: After MAX_RETRIES failed attempts for a single operand,
                or immediately if the input source is exhausted.
        """
        operands: list = []
        labels = ["first", "second"] if arity == 2 else [""]
        for label in labels[:arity]:
            prompt = f"Enter {label + ' ' if label else ''}operand: "
            last_error: ValueError | None = None
            for attempt in range(MAX_RETRIES):
                try:
                    raw = self._input_fn(prompt).strip()
                except StopIteration:
                    # Input source exhausted; re-raise the last conversion error
                    # if we have one, otherwise propagate StopIteration.
                    if last_error is not None:
                        raise last_error
                    raise
                try:
                    operands.append(coerce(raw))
                    last_error = None
                    break
                except (ValueError, TypeError):
                    last_error = ValueError(
                        f"Invalid operand '{raw}': expected a numeric value."
                    )
                    print(f"Error: {last_error}")
            else:
                # All MAX_RETRIES attempts exhausted without a valid value.
                raise ValueError("Too many invalid attempts for operand. Ending session.")
        return operands

    def _dispatch(self, op_key: str, operands: list) -> float | int:
        """Call the Calculator method corresponding to *op_key* with *operands*.

        Args:
            op_key: A key present in the OPERATIONS registry.
            operands: A list of already-coerced operand values.

        Returns:
            The result returned by the Calculator method.

        Raises:
            ValueError: Propagated from the Calculator method.
            ZeroDivisionError: Propagated from the Calculator method.
            TypeError: Propagated from the Calculator method.
        """
        method_name: str = OPERATIONS[op_key]["method"]
        method = getattr(self._calculator, method_name)
        return method(*operands)


def run_session(
    calculator: Calculator,
    input_fn: Callable[[str], str] | None = None,
) -> None:
    """Convenience function: create an InputHandler and start the session loop.

    Args:
        calculator: A Calculator instance to use for computation.
        input_fn: Optional injectable input callable; defaults to built-in
            ``input``.
    """
    handler = InputHandler(calculator, input_fn)
    handler.run()
