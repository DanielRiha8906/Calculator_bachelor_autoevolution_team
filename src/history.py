"""History tracking module for the calculator.

Provides ``OperationRecord`` (a dataclass capturing a single operation's
metadata) and ``OperationHistory`` (a container that accumulates records and
exposes a query/clear interface).
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class OperationRecord:
    """Immutable record of a single calculator operation.

    Attributes:
        operation_name: Human-readable name of the operation (e.g. ``"add"``).
        operands: Ordered list of input values passed to the operation.
        result: The value returned by the operation.
        timestamp: The ``datetime`` at which the operation was recorded.
    """

    operation_name: str
    operands: list
    result: object
    timestamp: datetime


class OperationHistory:
    """Maintains an ordered log of ``OperationRecord`` entries.

    Records are appended via ``add_record`` and can be retrieved as a
    defensive copy via ``get_history``.  The log can be wiped with
    ``clear_history``.
    """

    def __init__(self) -> None:
        self._records: list[OperationRecord] = []

    def add_record(
        self,
        operation_name: str,
        operands: list,
        result: object,
        timestamp: datetime,
    ) -> None:
        """Append a new operation record to the history.

        Args:
            operation_name: Name of the calculator operation.
            operands: List of input values used in the operation.
            result: The computed result of the operation.
            timestamp: The datetime at which the operation completed.
        """
        self._records.append(
            OperationRecord(
                operation_name=operation_name,
                operands=operands,
                result=result,
                timestamp=timestamp,
            )
        )

    def get_history(self) -> list[OperationRecord]:
        """Return a shallow copy of all recorded operations.

        Returns:
            A new list containing every ``OperationRecord`` in insertion order.
            Callers receive a copy, so mutations to the returned list do not
            affect the internal log.
        """
        return list(self._records)

    def clear_history(self) -> None:
        """Remove all records from the history log."""
        self._records.clear()

    def __len__(self) -> int:
        """Return the number of records currently in the history.

        Returns:
            Integer count of stored ``OperationRecord`` entries.
        """
        return len(self._records)
