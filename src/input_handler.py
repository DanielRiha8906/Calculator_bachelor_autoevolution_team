"""Interactive session loop for the Calculator application.

This module provides an operation registry, an InputHandler class that drives a
REPL-style session, and a convenience function for bootstrapping the session
from an external entry point.
"""

from __future__ import annotations

from typing import Callable

from .calculator import Calculator
from .validation import (
    MAX_RETRIES,
    RetryCounter,
    RetryExhausted,
    validate_operation,
    validate_operand,
)


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

# Sentinel returned by _prompt_for_operation when the user requests a session exit.
_EXIT_SENTINEL = object()


class _SessionExit(Exception):
    """Internal signal: user typed 'exit'/'quit' during operand collection."""


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
        self._retry_counter = RetryCounter()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Run the interactive session loop.

        Prints the operation menu, reads the user's choice, collects operands,
        dispatches to the Calculator, and prints the result.  The loop exits
        when the user enters "exit" or "quit" at the operation prompt, or when
        the retry limit (MAX_RETRIES) is exceeded for either the operation or
        operand input.
        Catches ValueError, ZeroDivisionError, and TypeError, printing a
        user-friendly message without crashing.
        """
        while True:
            try:
                op_choice = self._prompt_for_operation()
            except RetryExhausted:
                print("Too many invalid attempts. Ending session.")
                break

            if op_choice is _EXIT_SENTINEL:
                # User entered exit/quit; _prompt_for_operation already printed "Goodbye!"
                break

            op_info = OPERATIONS[op_choice]  # type: ignore[index]
            arity: int = op_info["arity"]
            coerce: Callable = op_info.get("coerce", float)  # type: ignore[assignment]

            try:
                operands = self._prompt_operands(arity, coerce)
            except RetryExhausted:
                print("Too many invalid attempts. Ending session.")
                break
            except _SessionExit:
                # User typed exit/quit while being prompted for an operand.
                print("Goodbye!")
                break

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

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _show_menu(self) -> None:
        """Print the list of available operations to stdout."""
        print("\nAvailable operations:")
        for key, info in OPERATIONS.items():
            print(f"  {key:<14} — {info['label']}")

    def _prompt_for_operation(self) -> object:
        """Show the menu and prompt for an operation, with retry logic.

        Displays the operation menu, reads user input, handles exit/quit,
        and validates the entered operation key.  On each invalid entry the
        retry counter for "operation" is incremented; on success it is reset.

        Returns:
            A validated, lowercased operation key (str) present in OPERATIONS,
            or ``_EXIT_SENTINEL`` if the user entered "exit" or "quit".

        Raises:
            RetryExhausted: When the number of consecutive invalid entries
                reaches MAX_RETRIES.
        """
        while True:
            self._show_menu()
            op_choice = self._input_fn(
                "Enter operation (or 'exit'/'quit' to stop): "
            ).strip().lower()

            if op_choice in ("exit", "quit"):
                print("Goodbye!")
                return _EXIT_SENTINEL

            try:
                validated = validate_operation(op_choice, OPERATIONS)
            except ValueError as exc:
                print(f"Error: {exc}")
                self._retry_counter.increment("operation")
                if self._retry_counter.is_exhausted("operation", MAX_RETRIES):
                    raise RetryExhausted("operation", MAX_RETRIES)
                continue

            self._retry_counter.reset("operation")
            return validated

    def _prompt_operands(self, arity: int, coerce: Callable = float) -> list:
        """Prompt the user for the required number of operands, with retry logic.

        For each required operand, re-prompts on invalid input until a valid
        value is entered or the retry limit (MAX_RETRIES) is reached.  If the
        user enters "exit" or "quit" during operand collection, a
        ``_SessionExit`` exception is raised to signal a graceful session
        termination.

        Args:
            arity: Number of operands to collect (1 or 2).
            coerce: Callable used to convert the raw string to a numeric value;
                defaults to ``float``.

        Returns:
            A list of converted operand values.

        Raises:
            RetryExhausted: When consecutive invalid attempts for a single
                operand reach MAX_RETRIES.
            _SessionExit: When the user enters "exit" or "quit" at an operand
                prompt.
        """
        operands: list = []
        labels = ["first", "second"] if arity == 2 else [""]
        for label in labels[:arity]:
            prompt = f"Enter {label + ' ' if label else ''}operand: "
            while True:
                raw = self._input_fn(prompt).strip()

                # Allow graceful exit during operand collection.
                if raw.lower() in ("exit", "quit"):
                    raise _SessionExit()

                try:
                    value = validate_operand(raw, coerce, operand_position=label)
                except ValueError as exc:
                    print(f"Error: {exc}")
                    self._retry_counter.increment("operand")
                    if self._retry_counter.is_exhausted("operand", MAX_RETRIES):
                        raise RetryExhausted("operand", MAX_RETRIES)
                    continue

                self._retry_counter.reset("operand")
                operands.append(value)
                break
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
