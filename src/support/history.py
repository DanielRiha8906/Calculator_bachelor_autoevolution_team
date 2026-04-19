"""Operation history management for the Calculator.

Provides persistent, per-session recording of calculator operations to a plain
text file.  History is cleared at session start for isolation and can be read
back for display in the interactive REPL.
"""

import sys
from typing import Optional


class OperationHistory:
    """Manage a flat-file operation history for calculator sessions.

    Each session begins with a fresh history file (created or truncated via
    ``clear_history``).  Individual operation entries are appended one per line
    via ``record_operation``.  The full history can be retrieved as a list of
    strings via ``display_history``.

    All file I/O errors are caught, logged to stderr, and silently swallowed so
    that history failures never interrupt the calculator session.

    Args:
        history_file: Path to the history file.  Defaults to ``"history.txt"``
            in the current working directory.
    """

    def __init__(self, history_file: str = "history.txt") -> None:
        self.history_file: str = history_file

    def clear_history(self) -> None:
        """Clear or create the history file.

        Truncates the file to zero bytes if it already exists, or creates an
        empty file if it does not.  Called once at session start to ensure
        isolation between calculator sessions.
        """
        try:
            with open(self.history_file, "w", encoding="utf-8") as fh:
                fh.truncate(0)
        except OSError as exc:
            print(
                f"Warning: could not clear history file {self.history_file!r}: {exc}",
                file=sys.stderr,
            )

    def record_operation(self, entry: str) -> None:
        """Append a single operation entry to the history file.

        The entry is written as-is followed by a newline.  If the file cannot
        be opened or written to, the error is logged to stderr and silently
        swallowed.

        Args:
            entry: A human-readable description of the operation, e.g.
                ``"add(2, 3) = 5"``.
        """
        try:
            with open(self.history_file, "a", encoding="utf-8") as fh:
                fh.write(entry + "\n")
        except OSError as exc:
            print(
                f"Warning: could not write to history file {self.history_file!r}: {exc}",
                file=sys.stderr,
            )

    def display_history(self) -> list[str]:
        """Read and return all recorded operation entries.

        Returns:
            A list of strings, one per recorded operation, with trailing
            newlines stripped.  Returns an empty list if the history file does
            not exist or cannot be read.
        """
        try:
            with open(self.history_file, "r", encoding="utf-8") as fh:
                return [line.rstrip("\n") for line in fh.readlines()]
        except FileNotFoundError:
            return []
        except OSError as exc:
            print(
                f"Warning: could not read history file {self.history_file!r}: {exc}",
                file=sys.stderr,
            )
            return []
