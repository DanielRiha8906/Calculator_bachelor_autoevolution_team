"""Operation history management for the Calculator application.

Provides a HistoryManager class that persists calculator operation records
to a file, enabling session history retrieval and cross-session isolation.
"""


class HistoryManager:
    """Manages persistent recording and retrieval of calculator operations.

    Records each completed operation as a formatted line in a history file.
    Supports clearing the file at session start to ensure cross-session
    isolation, and reading all recorded entries back as a list of strings.

    Args:
        history_file_path: Path to the file used to store history entries.
            Defaults to "history.txt". Pass a temporary path in tests.
    """

    def __init__(self, history_file_path: str = "history.txt") -> None:
        self.history_file_path = history_file_path

    def record_operation(
        self, operation_name: str, operands: list[float], result: float
    ) -> None:
        """Append a single operation record to the history file.

        Args:
            operation_name: Name of the operation (e.g. "add").
            operands: List of operand values used in the operation.
            result: The computed result of the operation.
        """
        line = self._format_operation(operation_name, operands, result)
        with open(self.history_file_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def get_history(self) -> list[str]:
        """Return all recorded operation entries as a list of formatted strings.

        Returns:
            A list of history entry strings, one per recorded operation.
            Returns an empty list if the history file does not exist or is empty.
        """
        try:
            with open(self.history_file_path, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
            return [line for line in lines if line]
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        """Truncate the history file to empty.

        Creates the file if it does not exist. Call this at session start to
        ensure cross-session isolation.
        """
        with open(self.history_file_path, "w", encoding="utf-8") as f:
            f.truncate(0)

    def _format_operation(
        self, operation_name: str, operands: list[float], result: float
    ) -> str:
        """Format an operation record as a human-readable string.

        Args:
            operation_name: Name of the operation (e.g. "add").
            operands: List of operand values used in the operation.
            result: The computed result of the operation.

        Returns:
            A string in the form "operation_name(operand1, operand2, ...) = result".
        """
        operand_str = ", ".join(str(o) for o in operands)
        return f"{operation_name}({operand_str}) = {result}"
