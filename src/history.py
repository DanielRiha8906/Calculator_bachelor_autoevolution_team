"""Persistent operation history for the calculator session."""

import os


class OperationHistory:
    """Records calculator operations to a file and provides display/clear utilities.

    Each operation is appended to the file as a plain text line. Line numbers
    are assigned dynamically at display time so that the file remains a simple
    append-only log.
    """

    def __init__(self, filename: str = "history.txt") -> None:
        """Initialise the history store with the given filename.

        Args:
            filename: Path to the file used for persistent storage.
        """
        self.filename: str = filename

    def record_operation(self, operation: str, operands: list, result: float) -> None:
        """Append one operation entry to the history file.

        The line is written without a line number; numbering is applied
        at display time so the raw file stays a simple append-only log.

        Args:
            operation: Name of the operation (e.g. ``"add"``).
            operands: List of operand values used in the operation.
            result: The computed result of the operation.
        """
        operands_str = ", ".join(str(o) for o in operands)
        line = f"{operation}({operands_str}) = {result}\n"
        with open(self.filename, "a", encoding="utf-8") as fh:
            fh.write(line)

    def display_history(self) -> str:
        """Return the full operation history as a numbered, human-readable string.

        Returns:
            A multi-line string with each operation prefixed by its 1-based
            index, or ``"No history yet."`` when the file is absent or empty.
        """
        if self.is_empty():
            return "No history yet."

        lines: list[str] = []
        with open(self.filename, "r", encoding="utf-8") as fh:
            for index, raw_line in enumerate(fh, start=1):
                stripped = raw_line.rstrip("\n")
                if stripped:
                    lines.append(f"{index}. {stripped}")

        return "\n".join(lines) if lines else "No history yet."

    def clear(self) -> None:
        """Delete the history file if it exists.

        No error is raised when the file is absent. Called at session startup
        to ensure a clean slate for each run.
        """
        try:
            os.remove(self.filename)
        except FileNotFoundError:
            pass

    def is_empty(self) -> bool:
        """Return True if the history file does not exist or contains no content.

        Returns:
            ``True`` when there is no recorded history, ``False`` otherwise.
        """
        if not os.path.exists(self.filename):
            return True
        return os.path.getsize(self.filename) == 0
