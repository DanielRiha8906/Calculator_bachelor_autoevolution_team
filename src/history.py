"""history.py — append-only in-memory log of calculator operations.

Provides two public types:

- ``OperationRecord``: frozen dataclass capturing a single operation event,
  including its timestamp, name, operands, and result.
- ``OperationHistory``: collection class managing an ordered sequence of
  ``OperationRecord`` instances with append, retrieval, and clear operations.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class OperationRecord:
    """Immutable record of a single calculator operation.

    Attributes:
        timestamp: Unix timestamp (seconds since epoch) at the moment the
            operation was recorded.
        operation: The operation name (e.g. ``"add"``, ``"factorial"``).
        operands: Ordered list of operand values passed to the operation.
        result: The computed numeric result of the operation.
    """

    timestamp: float
    operation: str
    operands: list
    result: Any


class OperationHistory:
    """Append-only, in-memory history of calculator operations.

    Records are stored in chronological order.  This class is not
    thread-safe; concurrent access requires external synchronisation.
    """

    def __init__(self) -> None:
        self._records: list[OperationRecord] = []

    def append(self, operation: str, operands: list, result: Any) -> None:
        """Add a new operation record with the current timestamp.

        Args:
            operation: The operation name (e.g. ``"add"``, ``"multiply"``).
            operands: The list of operand values used in the operation.
            result: The computed result of the operation.
        """
        record = OperationRecord(
            timestamp=time.time(),
            operation=operation,
            operands=operands,
            result=result,
        )
        self._records.append(record)

    def get_all(self) -> list[OperationRecord]:
        """Return all records in chronological order.

        Returns:
            A new list containing every ``OperationRecord`` in the order
            they were appended.
        """
        return list(self._records)

    def clear(self) -> None:
        """Remove all records from the history."""
        self._records.clear()

    def __len__(self) -> int:
        """Return the number of records currently stored."""
        return len(self._records)
