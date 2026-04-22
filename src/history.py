"""Operation history tracking for the Calculator.

Provides :class:`OperationHistory`, which records formatted strings for each
calculator operation performed during a session and supports writing the full
log to a file.
"""


class OperationHistory:
    """Accumulates a log of calculator operations performed during a session.

    Each recorded entry is a human-readable string of the form::

        operation_name(arg1, arg2) = result

    Entries are kept in insertion order and can be retrieved as a list,
    cleared, or written to a file.
    """

    def __init__(self) -> None:
        """Initialize with an empty entry list."""
        self._entries: list[str] = []

    def add_entry(self, operation_name: str, args: list, result: object) -> None:
        """Format and append one operation record to the history.

        Args:
            operation_name: The name of the calculator method that was called.
            args: The positional arguments that were passed to the method.
            result: The value returned by the method.
        """
        entry = self._format_entry(operation_name, args, result)
        self._entries.append(entry)

    def get_entries(self) -> list[str]:
        """Return a copy of the current history entries.

        Returns:
            A new list containing all recorded entry strings in insertion order.
        """
        return list(self._entries)

    def clear(self) -> None:
        """Remove all entries from the history."""
        self._entries = []

    def write_to_file(self, filepath: str) -> None:
        """Write all history entries to a file, one per line.

        The file is opened in write mode, overwriting any existing content.

        Args:
            filepath: Absolute or relative path to the destination file.
        """
        with open(filepath, "w", encoding="utf-8") as fh:
            for entry in self._entries:
                fh.write(entry + "\n")

    def _format_entry(self, operation_name: str, args: list, result: object) -> str:
        """Build a human-readable string for one operation record.

        Floats that are whole numbers (e.g. ``5.0``) are displayed without
        a decimal point (``5``).  All other values use :func:`repr`.

        Args:
            operation_name: The name of the calculator method.
            args: The positional arguments passed to the method.
            result: The value returned by the method.

        Returns:
            A formatted string such as ``"add(2, 3) = 5"`` or
            ``"sqrt(2) = 1.4142135623730951"``.
        """

        def _fmt_value(value: object) -> str:
            if isinstance(value, float) and not isinstance(value, bool):
                if value == int(value):
                    return str(int(value))
                return str(value)
            return repr(value)

        args_str = ", ".join(_fmt_value(a) for a in args)
        result_str = _fmt_value(result)
        return f"{operation_name}({args_str}) = {result_str}"
