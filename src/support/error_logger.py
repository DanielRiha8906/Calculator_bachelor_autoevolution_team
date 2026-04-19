"""Error logging mechanism for the Calculator.

Provides persistent, categorized recording of calculator errors to a plain
text file.  Errors are cleared at session start for isolation and can be read
back for inspection via ``get_errors``.
"""

import datetime
import sys


class ErrorLogger:
    """Manage a flat-file error log for calculator sessions.

    Each session begins with a fresh error log (created or truncated via
    ``clear_errors``).  Individual error entries are appended one per line via
    ``log_error``.  The full error log can be retrieved as a list of strings
    via ``get_errors``.

    Three error type constants are defined at class level to categorise errors:

    - ``INVALID_INPUT``: user-supplied input could not be parsed or is
      out of range before reaching a calculation.
    - ``UNSUPPORTED_OPERATION``: the requested operation is not recognised.
    - ``CALCULATION_ERROR``: a numeric/domain error raised during calculation
      (e.g. division by zero, math domain error, overflow).

    All file I/O errors are caught, logged to stderr, and silently swallowed so
    that error-logging failures never interrupt the calculator session.

    Args:
        error_file: Path to the error log file.  Defaults to ``"error.log"``
            in the current working directory.
    """

    INVALID_INPUT: str = "INVALID_INPUT"
    UNSUPPORTED_OPERATION: str = "UNSUPPORTED_OPERATION"
    CALCULATION_ERROR: str = "CALCULATION_ERROR"

    def __init__(self, error_file: str = "error.log") -> None:
        self.error_file: str = error_file

    def clear_errors(self) -> None:
        """Clear or create the error log file.

        Truncates the file to zero bytes if it already exists, or creates an
        empty file if it does not.  Called once at session start to ensure
        isolation between calculator sessions.
        """
        try:
            with open(self.error_file, "w", encoding="utf-8") as fh:
                fh.truncate(0)
        except OSError as exc:
            print(
                f"Warning: could not clear error log {self.error_file!r}: {exc}",
                file=sys.stderr,
            )

    def log_error(
        self,
        error_type: str,
        user_input: str,
        exception: Exception,
    ) -> None:
        """Append a single error entry to the error log file.

        The entry is written as a single line in the format::

            <ISO8601 timestamp> | <error_type> | input=<user_input> | <exception message>

        If the file cannot be opened or written to, the error is logged to
        stderr and silently swallowed.

        Args:
            error_type: One of the class-level constants ``INVALID_INPUT``,
                ``UNSUPPORTED_OPERATION``, or ``CALCULATION_ERROR``.
            user_input: The raw user input string that triggered the error.
            exception: The exception instance that was caught.
        """
        timestamp = datetime.datetime.now().isoformat()
        entry = (
            f"{timestamp} | {error_type} | input={user_input!r} | {exception}"
        )
        try:
            with open(self.error_file, "a", encoding="utf-8") as fh:
                fh.write(entry + "\n")
        except OSError as exc:
            print(
                f"Warning: could not write to error log {self.error_file!r}: {exc}",
                file=sys.stderr,
            )

    def get_errors(self) -> list[str]:
        """Read and return all recorded error entries.

        Returns:
            A list of strings, one per recorded error, with trailing newlines
            stripped.  Returns an empty list if the error log does not exist
            or cannot be read.
        """
        try:
            with open(self.error_file, "r", encoding="utf-8") as fh:
                return [line.rstrip("\n") for line in fh.readlines()]
        except FileNotFoundError:
            return []
        except OSError as exc:
            print(
                f"Warning: could not read error log {self.error_file!r}: {exc}",
                file=sys.stderr,
            )
            return []
