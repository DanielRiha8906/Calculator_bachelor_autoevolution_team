"""Operation history tracking for the Calculator session.

Records each successful operation as a formatted string and provides
persistence via plain-text file output.
"""


class OperationHistory:
    """Tracks the history of successful calculator operations.

    Each record stores a human-readable representation of the call and
    its result, e.g. ``add(2, 3) = 5`` or ``divide(7, 2) = 3.5``.

    Attributes:
        _entries: Ordered list of formatted history entry strings.
    """

    def __init__(self) -> None:
        """Initialise an empty history."""
        self._entries: list[str] = []

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def record_operation(
        self, operation_name: str, args: list, result: object
    ) -> None:
        """Append a formatted record of a successful operation.

        Args:
            operation_name: The name of the calculator method that was called.
            args: The list of arguments that were passed to the method.
            result: The value returned by the method.
        """
        entry = self._format_entry(operation_name, args, result)
        self._entries.append(entry)

    def get_history(self) -> list[str]:
        """Return a copy of all recorded history entries.

        Returns:
            A new list containing the history strings in insertion order.
        """
        return list(self._entries)

    def clear(self) -> None:
        """Reset the history, removing all recorded entries."""
        self._entries = []

    def save_to_file(self, filepath: str = "history.txt") -> None:
        """Write all history entries to a plain-text file.

        Each entry is written on its own line.  If the history is empty
        an empty file is created (or an existing file is truncated).

        Args:
            filepath: Destination file path.  Defaults to ``"history.txt"``
                in the current working directory.
        """
        with open(filepath, "w", encoding="utf-8") as fh:
            for entry in self._entries:
                fh.write(entry + "\n")

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _format_entry(
        operation_name: str, args: list, result: object
    ) -> str:
        """Format a single history entry as a human-readable string.

        Whole-number floats (e.g. ``2.0``) are displayed without the
        decimal point (``2``) to keep output concise.  Non-whole floats
        are displayed as-is (e.g. ``3.5``).

        Args:
            operation_name: Name of the calculator operation.
            args: Positional arguments that were supplied to the operation.
            result: The return value of the operation.

        Returns:
            A string of the form ``operation_name(arg1, arg2, ...) = result``.

        Examples:
            >>> OperationHistory._format_entry("add", [2, 3], 5)
            'add(2, 3) = 5'
            >>> OperationHistory._format_entry("divide", [7, 2], 3.5)
            'divide(7, 2) = 3.5'
            >>> OperationHistory._format_entry("sqrt", [9.0], 3.0)
            'sqrt(9) = 3'
        """
        def _fmt(value: object) -> str:
            """Format a single value, collapsing whole-number floats to int."""
            if isinstance(value, float) and value == int(value):
                return str(int(value))
            return str(value)

        formatted_args = ", ".join(_fmt(a) for a in args)
        formatted_result = _fmt(result)
        return f"{operation_name}({formatted_args}) = {formatted_result}"
