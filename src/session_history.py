"""In-memory session-scoped operation history.

History is non-persistent: it lives only for the duration of the process
and is not written to disk.  A new instance starts empty; calling
:meth:`clear` resets it back to that empty state.
"""


class SessionHistory:
    """Records calculator operations in memory for the duration of a session.

    No file I/O is performed — the history is discarded when the process exits.

    Example::

        history = SessionHistory()
        history.record_operation("add", [1.0, 2.0], 3.0)
        print(history.display_history())  # "1. add(1.0, 2.0) = 3.0"
    """

    def __init__(self) -> None:
        """Initialise an empty session history."""
        self._entries: list[dict] = []

    def record_operation(
        self, operation: str, operands: list, result: float
    ) -> None:
        """Append one operation entry to the in-memory history.

        Args:
            operation: Name of the operation (e.g. ``"add"``).
            operands: List of operand values used in the operation.
            result: The computed result of the operation.
        """
        self._entries.append(
            {"operation": operation, "operands": list(operands), "result": result}
        )

    def get_history(self) -> list[dict]:
        """Return all recorded entries as a list of dicts.

        Each dict contains the keys ``"operation"``, ``"operands"``, and
        ``"result"``.

        Returns:
            A copy of the internal entries list so callers cannot mutate it.
        """
        return list(self._entries)

    def display_history(self) -> str:
        """Return the history as a numbered, human-readable string.

        Returns:
            A multi-line string with each operation prefixed by its 1-based
            index, or ``"No history yet."`` when the history is empty.
        """
        if not self._entries:
            return "No history yet."

        lines: list[str] = []
        for index, entry in enumerate(self._entries, start=1):
            operands_str = ", ".join(str(o) for o in entry["operands"])
            lines.append(
                f"{index}. {entry['operation']}({operands_str}) = {entry['result']}"
            )
        return "\n".join(lines)

    def clear(self) -> None:
        """Remove all entries from the in-memory history."""
        self._entries.clear()

    def is_empty(self) -> bool:
        """Return True if no operations have been recorded yet.

        Returns:
            ``True`` when the history is empty, ``False`` otherwise.
        """
        return len(self._entries) == 0
