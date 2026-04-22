"""REPL state management for the Calculator interactive session.

Provides :class:`CalculatorSession`, which encapsulates state and control
flow for a calculator session loop without performing any I/O.  All methods
return results and optional error strings; they never call ``print`` or
``input`` directly.
"""

import inspect

from .calculator import Calculator
from .error_logger import ErrorLogger
from .history import OperationHistory
from .validation import (
    OperandValidationSession,
    OperationValidationSession,
)


class CalculatorSession:
    """Manages state and business logic for a calculator REPL session.

    This class owns the calculator instance, history tracker, error logger,
    and operation validation session.  It exposes methods that correspond to
    each step of the REPL loop.  No I/O (``print``/``input``) is performed
    inside this class — all output is returned as strings or delegated to the
    caller.

    Args:
        calculator: The :class:`~src.calculator.Calculator` instance used to
            execute operations.
    """

    def __init__(self, calculator: Calculator) -> None:
        self._calculator: Calculator = calculator
        self._history: OperationHistory = OperationHistory()
        self._error_logger: ErrorLogger = ErrorLogger()
        self._operation_list: list[str] = self._get_operation_list()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_operation_list(self) -> list[str]:
        """Return the current list of public operation names on the calculator."""
        return [
            name
            for name in dir(self._calculator)
            if not name.startswith("_") and callable(getattr(self._calculator, name))
        ]

    def _get_arity(self, op_name: str) -> int:
        """Return the number of operands required by *op_name*."""
        method = getattr(self._calculator, op_name)
        sig = inspect.signature(method)
        return len(sig.parameters)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def select_operation(
        self, raw_choice: str, mode: str
    ) -> tuple[str | None, int]:
        """Resolve a raw user choice to a canonical operation name.

        Handles both numeric shortcuts (``"1"``, ``"2"``, …) and direct
        name input.  Comparison against available operations is
        case-insensitive.

        This method also logs unsupported-operation events via the internal
        :class:`~src.error_logger.ErrorLogger`.

        Args:
            raw_choice: The raw string the user entered at the operation
                prompt.
            mode: ``'interactive'`` or ``'cli'`` — used to create the
                :class:`~src.validation.OperationValidationSession` that
                tracks retry counts (though the session object itself is
                not mutated here; retry tracking remains in the caller).

        Returns:
            A 2-tuple ``(op_name, exit_code)`` where:

            - ``op_name`` is the matched canonical operation name, or
              ``None`` if the choice was not recognised.
            - ``exit_code`` is ``0`` on success, ``1`` on unrecognised
              input, or ``2`` if the numeric index was out of range.
        """
        # Refresh operation list each call so it stays current.
        self._operation_list = self._get_operation_list()

        # Try to resolve a numeric shortcut.
        resolved_choice = raw_choice
        try:
            idx = int(raw_choice)
            if 1 <= idx <= len(self._operation_list):
                resolved_choice = self._operation_list[idx - 1]
            else:
                return None, 2
        except ValueError:
            pass  # not a number — treat as a name

        # Case-insensitive name lookup.
        ops_lower: dict[str, str] = {
            op.lower(): op for op in self._operation_list
        }
        matched = ops_lower.get(resolved_choice.lower())

        if matched is None:
            self._error_logger.log_unsupported_operation(resolved_choice)
            return None, 1

        return matched, 0

    def collect_operands(
        self, arity: int, mode: str
    ) -> tuple[list[float] | None, int]:
        """Collect the required number of numeric operands via a validation session.

        Operand prompts are produced internally using a lambda; the caller is
        not responsible for any I/O here.  This method wraps
        :class:`~src.validation.OperandValidationSession` and handles both
        interactive (retry) and CLI (fast-fail) modes.

        Args:
            arity: Number of operands to collect (1 or 2 for most operations).
            mode: ``'interactive'`` or ``'cli'``.

        Returns:
            A 2-tuple ``(operands, exit_code)`` where:

            - ``operands`` is a :class:`list` of :class:`float` values on
              success, or ``None`` if the retry limit was exceeded or a
              :class:`SystemExit` was raised.
            - ``exit_code`` is ``0`` on success, ``1`` on retry-limit
              exceeded, or ``2`` if :class:`SystemExit` was raised (CLI
              mode).
        """
        session = OperandValidationSession(mode=mode)
        operands: list[float] = []

        try:
            for i in range(1, arity + 1):
                value = session.validate_input(
                    prompt_fn=lambda idx=i: input(f"  Enter operand {idx}: "),
                    error_msg="Invalid input:",
                )
                if value is None:
                    # Interactive retry limit reached.
                    self._error_logger.log_invalid_operand(
                        "interactive-session",
                        "Maximum retry attempts exceeded for operand input.",
                    )
                    return None, 1
                operands.append(value)
        except SystemExit as exc:
            self._error_logger.log_invalid_operand(
                str(exc).split("'")[1] if "'" in str(exc) else "unknown",
                str(exc),
            )
            raise  # re-raise so CLI behaviour is preserved

        return operands, 0

    def execute_operation(
        self, op_name: str, operands: list[float]
    ) -> tuple[object, str | None]:
        """Execute a named calculator operation with the given operands.

        Args:
            op_name: The canonical name of the operation to call.
            operands: The list of float operand values.

        Returns:
            A 2-tuple ``(result, error_msg)`` where ``error_msg`` is
            ``None`` on success, or a descriptive string when a known
            exception occurs (:class:`ZeroDivisionError`,
            :class:`ValueError`, or any other :class:`Exception`).
        """
        try:
            result = getattr(self._calculator, op_name)(*operands)
            return result, None
        except ZeroDivisionError as exc:
            numerator = operands[0] if operands else float("nan")
            self._error_logger.log_division_by_zero(numerator)
            return None, str(exc)
        except ValueError as exc:
            operand_ctx = operands[0] if operands else float("nan")
            self._error_logger.log_invalid_domain(op_name, operand_ctx, str(exc))
            return None, str(exc)
        except Exception as exc:  # noqa: BLE001
            return None, str(exc)

    def get_arity(self, op_name: str) -> int:
        """Return the number of operands required by the named operation.

        Args:
            op_name: The canonical operation name.

        Returns:
            The operand count (``self`` excluded).
        """
        return self._get_arity(op_name)

    def record_history(
        self, op_name: str, operands: list[float], result: object
    ) -> None:
        """Record a successful operation in the session history.

        Args:
            op_name: The name of the operation that was executed.
            operands: The operand values that were passed to the operation.
            result: The value returned by the operation.
        """
        self._history.record_operation(op_name, operands, result)

    def get_history(self) -> list[str]:
        """Return all recorded history entries.

        Returns:
            A list of formatted history strings in insertion order.
        """
        return self._history.get_history()

    def save_history(self, filepath: str) -> None:
        """Persist the operation history to a plain-text file.

        Args:
            filepath: Destination file path.
        """
        self._history.save_to_file(filepath)

    def get_operation_list(self) -> list[str]:
        """Return the current list of available operation names.

        Returns:
            A list of public method name strings from the calculator.
        """
        self._operation_list = self._get_operation_list()
        return list(self._operation_list)

    @property
    def max_retries(self) -> int:
        """Maximum retry attempts used by the operation validation session."""
        from .validation import _MAX_RETRIES_DEFAULT
        return _MAX_RETRIES_DEFAULT
