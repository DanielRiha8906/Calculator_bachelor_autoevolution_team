"""Interaction layer service — operation history.

Records and persists calculator operation history for user review. Part of
the interaction layer; has no direct role in arithmetic computation.

Records each successful operation to an in-memory list and to a persistent
``history.txt`` file in the current working directory.  The file is cleared
(or created) when the :class:`OperationHistory` instance is initialised, so
each session starts with a clean slate on disk while the in-memory list grows
throughout the session.
"""

from __future__ import annotations

# File path relative to CWD where history is persisted.
HISTORY_FILE: str = "history.txt"

# Unary operation keys — used to choose the formatting style.
_UNARY_OPERATIONS: frozenset[str] = frozenset({
    "factorial",
    "square",
    "cube",
    "square_root",
    "cube_root",
    "log",
    "ln",
})


class OperationHistory:
    """Tracks calculator operations performed during a session.

    On construction the backing ``history.txt`` file is cleared (or created
    empty).  Each successful operation is appended both to an in-memory list
    and to the file so the history survives beyond the process if needed.

    Attributes:
        _history: Ordered list of formatted operation strings.
        _file_path: Absolute or relative path to the history file.
    """

    def __init__(self) -> None:
        """Initialise an empty history and clear the history file."""
        self._history: list[str] = []
        self._file_path: str = HISTORY_FILE
        # Create or truncate the file so each session starts clean.
        with open(self._file_path, "w", encoding="utf-8") as fh:
            pass  # intentionally empty — file is cleared on __init__

    def record_operation(
        self,
        operation: str,
        operands: list[float],
        result: float,
    ) -> None:
        """Record a successful operation to memory and disk.

        Args:
            operation: The operation key (e.g. ``"add"``, ``"square_root"``).
            operands: The list of operands used (one for unary, two for binary).
            result: The numeric result returned by the operation.
        """
        entry = self._format_entry(operation, operands, result)
        self._history.append(entry)
        with open(self._file_path, "a", encoding="utf-8") as fh:
            fh.write(entry + "\n")

    def get_history(self) -> list[str]:
        """Return all recorded operation strings in chronological order.

        Returns:
            A list of formatted operation strings.  Returns an empty list when
            no operations have been recorded yet.
        """
        return list(self._history)

    def clear(self) -> None:
        """Clear the in-memory history list.

        Note:
            This does **not** truncate the history file.  The file is only
            cleared when a new :class:`OperationHistory` is instantiated.
        """
        self._history = []

    def _format_entry(
        self,
        operation: str,
        operands: list[float],
        result: float,
    ) -> str:
        """Format a single operation entry as a human-readable string.

        Binary operations are formatted as::

            operand1 operation operand2 = result

        Unary operations are formatted as::

            operation(operand) = result

        Args:
            operation: The operation key string.
            operands: The list of operands.
            result: The numeric result of the operation.

        Returns:
            A formatted string representing the operation.
        """
        if operation in _UNARY_OPERATIONS:
            return f"{operation}({operands[0]}) = {result}"
        # Binary operation — two operands.
        return f"{operands[0]} {operation} {operands[1]} = {result}"
