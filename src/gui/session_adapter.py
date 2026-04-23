"""Bridge between CalculatorSession and GUI event handlers.

:class:`GUISessionAdapter` wraps a :class:`~src.session.CalculatorSession`
and translates its return conventions into GUI-friendly ``(result_str, error_msg)``
tuples, so window code never needs to inspect raw session internals.
"""

from ..session import CalculatorSession


class GUISessionAdapter:
    """Adapts a :class:`~src.session.CalculatorSession` for GUI consumption.

    All computation is fully delegated to the wrapped session instance.
    This class only converts data shapes and absorbs error handling into
    the ``(result_str, error_msg)`` convention used by the GUI.

    Args:
        session: An initialised :class:`~src.session.CalculatorSession`.
    """

    def __init__(self, session: CalculatorSession) -> None:
        self._session: CalculatorSession = session
        self._pending_operand1: float | None = None

    def store_first_operand(self, value: float) -> None:
        """Save *value* as the first operand for a pending binary operation.

        Args:
            value: The numeric value to store.
        """
        self._pending_operand1 = value

    def get_pending_operand(self) -> float | None:
        """Retrieve the stored first operand, or ``None`` if none is pending.

        Returns:
            The stored operand value, or ``None`` if no operand has been saved.
        """
        return self._pending_operand1

    def clear_pending_operand(self) -> None:
        """Clear the stored first operand.

        Should be called on mode switch or error to reset pending state.
        """
        self._pending_operand1 = None

    def execute_operation_safe(
        self, op_name: str, operands: list, use_pending: bool = False
    ) -> tuple[str, str]:
        """Execute *op_name* with *operands* and return a display-ready result pair.

        On success the first element is the formatted result string and the
        second is an empty string.  On failure the first element is an empty
        string and the second contains the error description.

        The history is recorded automatically on success.

        Args:
            op_name: The canonical operation name (e.g. ``"add"``).
            operands: A list of numeric values (``int`` or ``float``).
            use_pending: When ``True`` and *operands* has exactly one element,
                the stored ``_pending_operand1`` is prepended to produce a
                two-element list before execution.  If ``_pending_operand1``
                is ``None`` the call proceeds without prepending, and the
                underlying session will return an arity error as normal.

        Returns:
            A 2-tuple ``(result_str, error_msg)`` where exactly one of the
            two strings is non-empty.
        """
        resolved_operands: list = operands
        if use_pending and len(operands) == 1 and self._pending_operand1 is not None:
            resolved_operands = [self._pending_operand1] + list(operands)

        result, error_msg = self._session.execute_operation(op_name, resolved_operands)
        if error_msg is not None:
            return "", error_msg
        self._session.record_history(op_name, resolved_operands, result)
        return str(result), ""

    def set_mode(self, mode_name: str) -> None:
        """Switch the session to *mode_name*.

        Args:
            mode_name: A string such as ``"normal"`` or ``"scientific"``.
        """
        self._session.set_mode(mode_name)

    def get_operations(self) -> list[str]:
        """Return the mode-filtered list of available operation names.

        Returns:
            A list of canonical operation name strings for the current mode.
        """
        return self._session.get_operation_list()

    def get_history(self) -> list[str]:
        """Return all history entries formatted for display.

        Returns:
            A list of human-readable history entry strings in insertion order.
        """
        return self._session.get_history()

    def clear_history(self) -> None:
        """Clear all recorded history entries from the session."""
        self._session._history.clear()

    def get_arity(self, op_name: str) -> int:
        """Return the number of operands required by *op_name*.

        Args:
            op_name: The canonical operation name.

        Returns:
            The operand count (1 for unary, 2 for binary).
        """
        return self._session.get_arity(op_name)
