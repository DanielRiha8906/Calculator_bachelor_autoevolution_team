"""Operation history tracking, formatting, display, and file persistence."""

import sys
from typing import Any


def format_history_entry(operation_name: str, operands: tuple, result: Any) -> str:
    """Format a single history entry as a human-readable string.

    Args:
        operation_name: The name of the operation (e.g. ``"add"``).
        operands: A tuple of operand values passed to the operation.
        result: The computed result of the operation.

    Returns:
        A string in the form ``"operation_name(arg1, arg2, ...) = result"``.
    """
    args_str = ", ".join(str(o) for o in operands)
    return f"{operation_name}({args_str}) = {result}"


class OperationHistory:
    """Tracks a session's successful calculator operations.

    Each successful operation is appended to an in-memory list of formatted
    strings.  The list can be displayed, inspected, or persisted to a file.
    Instances are independent — no shared state between ``OperationHistory``
    objects.
    """

    def __init__(self) -> None:
        """Initialise an empty history."""
        self._entries: list[str] = []

    def record(self, operation_name: str, operands: tuple, result: Any) -> None:
        """Append a formatted entry for a successful operation.

        Args:
            operation_name: The name of the operation (e.g. ``"add"``).
            operands: A tuple of operand values passed to the operation.
            result: The computed result of the operation.
        """
        self._entries.append(format_history_entry(operation_name, operands, result))

    def get_entries(self) -> list[str]:
        """Return the list of recorded history entries.

        Returns:
            A list of formatted strings, one per recorded operation, in
            chronological order.
        """
        return list(self._entries)

    def display(self) -> str:
        """Return the history as a multi-line formatted string.

        Returns:
            ``"No operations recorded"`` when the history is empty; otherwise a
            newline-joined string of all recorded entries in chronological order.
        """
        if not self._entries:
            return "No operations recorded"
        return "\n".join(self._entries)

    def write_to_file(self, filepath: str = "history.txt") -> None:
        """Persist the current history to a file.

        Overwrites any existing content at *filepath*.  If the file cannot be
        written (e.g. permission denied, directory does not exist) the error is
        logged to ``stderr`` and the method returns without raising.

        Args:
            filepath: Destination path for the history file.  Defaults to
                ``"history.txt"`` in the current working directory.
        """
        content = "\n".join(self._entries)
        try:
            with open(filepath, "w", encoding="utf-8") as fh:
                fh.write(content)
        except OSError as exc:
            print(f"Warning: could not write history to '{filepath}': {exc}", file=sys.stderr)
