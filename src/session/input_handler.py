"""Interactive session loop for the Calculator application.

This module provides an InputHandler class that drives a REPL-style session,
and a convenience function for bootstrapping the session from an external
entry point.

The operation registry (``OPERATIONS``) is defined in ``src/operations/``
and imported here; this module re-exports it for backwards compatibility with
any existing code that imports ``OPERATIONS`` from ``input_handler``.
"""

from __future__ import annotations

from typing import Callable

from ..core.calculator import Calculator
from ..shared.dispatcher import OperationDispatcher
from ..shared.logger import Logger
from ..operations import OPERATIONS
from .base_mode import BaseMode
from .history import History
from .mode import Mode, parse_mode_command


# Maximum number of consecutive invalid inputs before the session is terminated.
MAX_RETRIES: int = 5


class InputHandler:
    """Drives an interactive calculator session.

    Args:
        calculator: A Calculator instance to which operations are dispatched.
        input_fn: Callable used to read user input; defaults to the built-in
            ``input``. Inject a custom callable in tests to avoid touching
            ``builtins.input``.
        logger: Optional ``Logger`` instance for error logging.  When ``None``
            (the default), a ``Logger`` is created lazily inside ``run()``
            so that construction-time callers (e.g. tests) are not forced to
            deal with log file creation.
    """

    def __init__(
        self,
        calculator: Calculator,
        input_fn: Callable[[str], str] | None = None,
        logger: Logger | None = None,
    ) -> None:
        self._calculator = calculator
        self._input_fn: Callable[[str], str] = input_fn if input_fn is not None else input
        self._history = History()
        self._logger: Logger | None = logger
        self._dispatcher = OperationDispatcher(calculator)
        self._mode: Mode = Mode.NORMAL
        self._mode_handler = BaseMode()

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

        Users may switch modes by entering ``"mode normal"`` or
        ``"mode scientific"`` at the operation prompt.
        """
        if self._logger is None:
            self._logger = Logger()

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

                # Handle mode-switch commands before anything else.
                mode_result = parse_mode_command(op_choice)
                if mode_result is not None:
                    self._mode = mode_result
                    print(f"Mode switched to: {self._mode.value.capitalize()}")
                    continue

                if op_choice == "history":
                    entries = self._history.get_all()
                    if entries:
                        print("\n".join(entries))
                    else:
                        print("No history yet.")
                    continue

                available_ops = self._get_available_operations_for_mode()

                if op_choice not in OPERATIONS:
                    op_attempts += 1
                    self._logger.log_unsupported_operation(op_choice)
                    print(f"Error: Unknown operation '{op_choice}'. Please choose from the menu.")
                    print("Available operations: " + ", ".join(available_ops.keys()))
                    if op_attempts >= MAX_RETRIES:
                        print("Too many invalid attempts. Ending session.")
                        break
                    continue

                # Operation exists globally — check if it is accessible in the
                # current mode.
                if op_choice not in available_ops:
                    print(
                        f"Error: '{op_choice}' is only available in scientific mode. "
                        "Type 'mode scientific' to switch."
                    )
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
                    self._logger.log_division_by_zero(operands)
                    print("Error: Division by zero is not allowed.")
                    continue
                except ValueError as exc:
                    self._logger.log_domain_error(op_choice, str(exc))
                    print(f"Error: {exc}")
                    continue
                except TypeError as exc:
                    self._logger.log_domain_error(op_choice, str(exc))
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

    def _get_available_operations_for_mode(self) -> dict:
        """Return the subset of OPERATIONS accessible in the current mode.

        In NORMAL mode only the keys present in NORMAL_OPERATIONS are returned.
        In SCIENTIFIC mode the full unified OPERATIONS dict is returned,
        exposing both normal and scientific operations.

        Delegates filtering logic to the composed :class:`BaseMode` instance.

        Returns:
            A dict mapping operation keys to their registry entries for the
            current mode.
        """
        return self._mode_handler.get_available_operations(self._mode)

    def _show_menu(self) -> None:
        """Print the list of available operations to stdout.

        The header reflects the current mode, and only operations accessible
        in that mode are listed.
        """
        mode_label = self._mode.value.capitalize()
        print(f"\nAvailable operations ({mode_label} Mode):")
        for key, info in self._get_available_operations_for_mode().items():
            print(f"  {key:<14} — {info['label']}")
        print("  (type 'mode normal' or 'mode scientific' to switch modes)")

    def _prompt_operands(self, arity: int, coerce: Callable = float) -> list:
        """Prompt the user for the required number of operands.

        For each operand position, up to MAX_RETRIES attempts are made.  On
        each failed coerce attempt the error is printed and the same operand is
        re-prompted.  After MAX_RETRIES consecutive failures for a single
        operand a ValueError is raised to abort the current operation.

        Delegates the actual type coercion to
        ``self._dispatcher.coerce_operands()``.

        Args:
            arity: Number of operands to collect (0, 1, or 2).
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
                    coerced = self._dispatcher.coerce_operands([raw], coerce)
                    operands.extend(coerced)
                    last_error = None
                    break
                except ValueError as exc:
                    last_error = exc
                    if self._logger is not None:
                        self._logger.log_invalid_operand(raw, "<numeric>")
                    print(f"Error: {last_error}")
            else:
                # All MAX_RETRIES attempts exhausted without a valid value.
                raise ValueError("Too many invalid attempts for operand. Ending session.")
        return operands

    def _dispatch(self, op_key: str, operands: list) -> float | int:
        """Call the Calculator method corresponding to *op_key* with *operands*.

        Delegates to ``self._dispatcher.dispatch()``.

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
        return self._dispatcher.dispatch(op_key, operands)


def run_session(
    calculator: Calculator,
    input_fn: Callable[[str], str] | None = None,
    logger: Logger | None = None,
) -> None:
    """Convenience function: create an InputHandler and start the session loop.

    Args:
        calculator: A Calculator instance to use for computation.
        input_fn: Optional injectable input callable; defaults to built-in
            ``input``.
        logger: Optional ``Logger`` instance for error logging.  When ``None``
            (the default), the ``InputHandler`` creates one lazily on first
            call to ``run()``.
    """
    handler = InputHandler(calculator, input_fn, logger)
    handler.run()
