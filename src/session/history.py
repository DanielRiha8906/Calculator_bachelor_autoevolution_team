"""Session-scoped operation history tracker for the Calculator application.

This module provides the History class, which records calculator operations
as they are executed in an interactive session, formats them in function-call
notation, allows on-demand display, and persists entries to a file on session
end.
"""

from __future__ import annotations


class History:
    """Tracks calculator operations for a single interactive session.

    Each recorded operation is stored as a formatted string in the form
    ``operation(arg1, arg2, ...) = result``.  The list grows monotonically
    during a session and is written to disk when the session ends.

    Attributes:
        _operations: Ordered list of formatted history entry strings.
    """

    def __init__(self) -> None:
        """Initialize an empty operation history."""
        self._operations: list[str] = []

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def add_operation(
        self,
        operation_name: str,
        operands: list,
        result: float | int,
    ) -> None:
        """Record a completed operation.

        Formats the entry via :meth:`_format_entry` and appends it to the
        internal operations list.

        Args:
            operation_name: The name of the operation (e.g. ``"add"``).
            operands: The operand values passed to the operation.
            result: The value returned by the operation.
        """
        entry = self._format_entry(operation_name, operands, result)
        self._operations.append(entry)

    def get_all(self) -> list[str]:
        """Return all formatted history entries.

        Returns:
            A shallow copy of the internal operations list so callers cannot
            mutate session history directly.
        """
        return list(self._operations)

    def save_to_file(self, filepath: str) -> None:
        """Write all history entries to a file, one entry per line.

        If the operations list is empty, an empty file is created.

        Args:
            filepath: Path of the output file.  Created or overwritten.

        Raises:
            OSError: Propagated if the file cannot be opened or written.
        """
        with open(filepath, "w", encoding="utf-8") as fh:
            for entry in self._operations:
                fh.write(entry + "\n")

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _format_entry(
        self,
        operation_name: str,
        operands: list,
        result: float | int,
    ) -> str:
        """Format a single history entry as ``operation(arg1, arg2, ...) = result``.

        Args:
            operation_name: The name of the operation.
            operands: The operand values used in the operation.
            result: The result of the operation.

        Returns:
            A human-readable string representation of the operation.
        """
        args_str = ", ".join(str(op) for op in operands)
        return f"{operation_name}({args_str}) = {result}"
