"""CLI dispatcher for the Calculator application.

This module provides the CliDispatcher class, which parses command-line
arguments and dispatches a single calculation to the Calculator, printing
the result to stdout or an error message to stderr.

Typical usage::

    python main.py add 5 7
    python main.py factorial 5
"""

from __future__ import annotations

import sys
from typing import Callable

from ..core.calculator import Calculator
from ..shared.dispatcher import OperationDispatcher
from ..shared.logger import Logger
from ..operations import OPERATIONS


class CliDispatcher:
    """Parse command-line arguments and dispatch a single calculation.

    Args:
        calculator: A Calculator instance to which operations are dispatched.
        logger: Optional ``Logger`` instance for error logging.  When ``None``
            (the default), a ``Logger`` is created lazily inside
            ``dispatch_from_args()`` so that construction-time callers (e.g.
            tests) are not forced to deal with log file creation.
    """

    def __init__(
        self,
        calculator: Calculator,
        logger: Logger | None = None,
    ) -> None:
        self._calculator = calculator
        self._logger: Logger | None = logger
        self._dispatcher = OperationDispatcher(calculator)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def dispatch_from_args(self, args: list[str]) -> int:
        """Parse *args*, execute the requested operation, and print the result.

        The expected argument format is::

            <operation> <operand1> [<operand2>]

        Results are printed to stdout.  Error messages are printed to stderr.

        Args:
            args: A list of string arguments, typically ``sys.argv[1:]``.

        Returns:
            0 on success, 1 on any error (unknown operation, wrong operand
            count, coercion failure, domain error, division by zero, or
            type error).
        """
        if self._logger is None:
            self._logger = Logger()

        if not args:
            self._print_error(
                "Usage: python main.py <operation> <operand1> [<operand2>]\n"
                f"Available operations: {', '.join(OPERATIONS.keys())}"
            )
            return 1

        op_key = args[0].lower()

        if op_key not in OPERATIONS:
            self._logger.log_unsupported_operation(op_key)
            self._print_error(
                f"Unknown operation '{op_key}'. "
                f"Available operations: {', '.join(OPERATIONS.keys())}"
            )
            return 1

        op_info = OPERATIONS[op_key]
        arity: int = op_info["arity"]
        coerce: Callable = op_info.get("coerce", float)  # type: ignore[assignment]

        operand_args = args[1:]
        if len(operand_args) != arity:
            self._logger.log_invalid_argument_count(op_key, arity, len(operand_args))
            self._print_error(
                f"Operation '{op_key}' requires {arity} operand(s), "
                f"but {len(operand_args)} were given."
            )
            return 1

        try:
            operands = self._coerce_operands(operand_args, coerce)
        except ValueError as exc:
            self._print_error(str(exc))
            return 1

        try:
            result = self._dispatch(op_key, operands)
        except ZeroDivisionError:
            self._logger.log_division_by_zero(operands)
            self._print_error("Division by zero is not allowed.")
            return 1
        except ValueError as exc:
            self._logger.log_domain_error(op_key, str(exc))
            self._print_error(str(exc))
            return 1
        except TypeError as exc:
            self._logger.log_domain_error(op_key, str(exc))
            self._print_error(str(exc))
            return 1

        print(result)
        return 0

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _coerce_operands(self, raw_args: list[str], coerce: Callable) -> list:
        """Convert a list of raw string arguments to numeric operands.

        Iterates over *raw_args* one at a time, delegating each single-element
        conversion to ``self._dispatcher.coerce_operands()`` so that any
        invalid operand can be logged before the error is propagated.

        Args:
            raw_args: Raw string operands from the command line.
            coerce: Callable used to convert each string (e.g. ``float`` or
                ``int``).

        Returns:
            A list of converted operand values.

        Raises:
            ValueError: If any operand string cannot be converted by *coerce*.
        """
        operands: list = []
        for raw in raw_args:
            try:
                coerced = self._dispatcher.coerce_operands([raw], coerce)
                operands.extend(coerced)
            except ValueError:
                if self._logger is not None:
                    self._logger.log_invalid_operand(raw, "<numeric>")
                raise ValueError(
                    f"Invalid operand '{raw}': expected a numeric value."
                )
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

    @staticmethod
    def _print_error(message: str) -> None:
        """Write *message* to stderr, prefixed with 'Error: '.

        Args:
            message: The human-readable error description.
        """
        print(f"Error: {message}", file=sys.stderr)
