"""Reusable operation dispatcher for the Calculator application.

This module provides ``OperationDispatcher``, a helper class that centralises
the two pieces of dispatch logic previously duplicated between
``InputHandler`` (interactive mode) and ``CliDispatcher`` (CLI mode):

1. Coercing raw string operands to numeric values.
2. Resolving and invoking the correct ``Calculator`` method by name.

Both interaction modes compose an ``OperationDispatcher`` instance rather
than reimplementing these behaviours independently.  Error handling (logging,
printing messages to the user) remains the caller's responsibility so that
this class stays free of any I/O or interface concerns.
"""

from __future__ import annotations

from typing import Callable

from ..core.calculator import Calculator


class OperationDispatcher:
    """Encapsulate operand coercion and Calculator method dispatch.

    Args:
        calculator: The ``Calculator`` instance to which operations are
            delegated.
    """

    def __init__(self, calculator: Calculator) -> None:
        self._calculator: Calculator = calculator

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def coerce_operands(self, raw_args: list[str], coerce: Callable) -> list:
        """Convert a list of raw string arguments to numeric operands.

        Iterates over *raw_args* and applies *coerce* to each element.  The
        first conversion failure immediately raises ``ValueError``; subsequent
        elements are not processed.

        Args:
            raw_args: Raw string operands supplied by the caller (from CLI
                arguments or interactive input).
            coerce: Callable used to convert each string to a numeric value
                (e.g. ``float`` or ``int``).

        Returns:
            A list of converted operand values in the same order as
            *raw_args*.

        Raises:
            ValueError: If any element of *raw_args* cannot be converted by
                *coerce*.
        """
        operands: list = []
        for raw in raw_args:
            try:
                operands.append(coerce(raw))
            except (ValueError, TypeError):
                raise ValueError(
                    f"Invalid operand '{raw}': expected a numeric value."
                )
        return operands

    def dispatch(self, op_key: str, operands: list) -> float | int:
        """Call the Calculator method identified by *op_key* with *operands*.

        Looks up the method name in the OPERATIONS registry (via the
        ``op_key``), resolves the method on the stored Calculator instance
        using ``getattr``, and invokes it with the supplied operands.

        Args:
            op_key: A key present in the OPERATIONS registry whose ``method``
                value names a public method on ``Calculator``.
            operands: A list of already-coerced operand values.

        Returns:
            The numeric result returned by the Calculator method.

        Raises:
            ValueError: Propagated from the Calculator method (domain error).
            ZeroDivisionError: Propagated from the Calculator method.
            TypeError: Propagated from the Calculator method.
        """
        from ..operations import OPERATIONS  # local import avoids any future circular-import risk

        method_name: str = OPERATIONS[op_key]["method"]
        method = getattr(self._calculator, method_name)
        return method(*operands)
