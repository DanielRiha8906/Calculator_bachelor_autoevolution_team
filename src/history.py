"""Operation history tracking and persistence for the calculator.

Provides the OperationHistory class which records successful calculator
operations both in-memory and to a file, with session isolation (each new
OperationHistory instance clears the file).
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class OperationHistory:
    """Tracks and persists calculator operation history for a single session.

    Each new instance starts with an empty history and overwrites the
    backing file so that sessions are fully isolated.

    Args:
        file_path: Path to the history file.  If None, defaults to
            "history.txt" in the current working directory.
    """

    def __init__(self, file_path: str | None = None) -> None:
        """Initialise a new session history.

        Args:
            file_path: Optional path for the history file.  Defaults to
                ``"history.txt"`` in the current working directory when None.
        """
        self._file_path: Path = Path(file_path) if file_path is not None else Path("history.txt")
        self._entries: list[str] = []

        # Clear / create the file at session start for session isolation.
        try:
            self._file_path.write_text("")
        except OSError as exc:
            logger.warning("Could not initialise history file %s: %s", self._file_path, exc)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def record(self, operation: str, operands: list[int | float], result: int | float) -> None:
        """Record a successful operation to in-memory history and the file.

        Args:
            operation: The name of the operation (e.g. ``"add"``).
            operands: The list of operands passed to the operation.
            result: The result returned by the operation.
        """
        line = self._format_operation(operation, operands, result)
        self._entries.append(line)
        self._write_to_file(line)

    def get_all(self) -> list[str]:
        """Return all recorded operations as formatted strings.

        Returns:
            A list of formatted operation strings (without trailing newlines).
            The list is in chronological order.
        """
        return list(self._entries)

    def clear(self) -> None:
        """Clear in-memory history and reset the backing file."""
        self._entries = []
        try:
            self._file_path.write_text("")
        except OSError as exc:
            logger.warning("Could not clear history file %s: %s", self._file_path, exc)

    def display(self) -> str:
        """Return a human-readable string representation of the history.

        Returns:
            A newline-separated string of numbered entries, or a message
            indicating the history is empty when no entries exist.
        """
        if not self._entries:
            return "History: (empty)"
        lines = [f"{i}. {entry}" for i, entry in enumerate(self._entries, 1)]
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _format_operation(
        self,
        operation: str,
        operands: list[int | float],
        result: int | float,
    ) -> str:
        """Format an operation record as a human-readable string.

        Args:
            operation: The operation name.
            operands: The operands (one for unary, two for binary operations).
            result: The computed result.

        Returns:
            A string of the form ``"operation operand1 operand2 = result"``
            (space-separated), or ``"operation operand1 = result"`` for unary
            operations.
        """
        operands_str = " ".join(str(op) for op in operands)
        return f"{operation} {operands_str} = {result}"

    def _write_to_file(self, line: str) -> None:
        """Append a single entry line to the history file.

        File I/O errors are logged but do not propagate to the caller.

        Args:
            line: The formatted operation string to append (without newline).
        """
        try:
            with self._file_path.open("a", encoding="utf-8") as fh:
                fh.write(line + "\n")
        except OSError as exc:
            logger.warning("Could not write to history file %s: %s", self._file_path, exc)
