"""History tracking for the Calculator application.

This is the canonical location for the ``HistoryTracker`` class, which
records each calculator operation performed during an interactive session,
supports in-session display, and persists the log to a file when the
session ends.
"""

from __future__ import annotations

import sys


class HistoryTracker:
    """Records and persists calculator operation history for a single session.

    Each entry is stored as a human-readable string in the format::

        operation_name(arg1, arg2, ...) = result

    Examples:
        >>> tracker = HistoryTracker()
        >>> tracker.record("add", [1, 2], 3)
        >>> tracker.get_history()
        ['add(1, 2) = 3']
    """

    def __init__(self) -> None:
        """Initialise an empty history list."""
        self._history: list[str] = []

    def record(self, operation_name: str, operands: list, result: object) -> None:
        """Append a new operation entry to the history.

        Args:
            operation_name: The name of the operation (e.g. ``"add"``).
            operands: The list of operand values passed to the operation.
            result: The value returned by the operation.

        Returns:
            None
        """
        args = ", ".join(str(o) for o in operands)
        entry = f"{operation_name}({args}) = {result}"
        self._history.append(entry)

    def get_history(self) -> list[str]:
        """Return a copy of the current history list.

        Returns:
            A new list containing all recorded history entries in order.
        """
        return list(self._history)

    def display(self) -> None:
        """Print the session history to stdout.

        If no operations have been recorded yet, a placeholder message is
        printed instead.

        Returns:
            None
        """
        if not self._history:
            print("No history for this session.")
            return
        print("Session history:")
        for entry in self._history:
            print(f"  {entry}")

    def save_to_file(self, filepath: str = "history.txt") -> None:
        """Write all history entries to a plain-text file, one per line.

        If the file cannot be written (e.g. permission error), a warning is
        printed to stderr and the exception is suppressed so the session can
        exit cleanly.

        Args:
            filepath: Destination file path. Defaults to ``"history.txt"``
                in the current working directory.

        Returns:
            None
        """
        try:
            with open(filepath, "w") as f:
                for entry in self._history:
                    f.write(entry + "\n")
        except OSError as e:
            print(f"Warning: could not save history: {e}", file=sys.stderr)

    def clear(self) -> None:
        """Remove all entries from the history.

        Returns:
            None
        """
        self._history.clear()
