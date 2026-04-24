"""Error logging module for the calculator application.

Provides :class:`ErrorLog`, a lightweight logger that appends structured
error entries to a plain-text file.  The file is created lazily on the
first call to :meth:`ErrorLog.log_error`; instantiation itself never
touches the filesystem.
"""

import datetime
import pathlib


class ErrorLog:
    """Append-only error log backed by a plain-text file.

    Each log entry is a single line with five pipe-separated fields::

        <ISO8601_UTC_timestamp> | <error_category> | <operation> | <inputs> | <error_description>

    The file is created (or appended to) on the first call to
    :meth:`log_error`.  If a write fails for any reason the exception is
    silently swallowed so that a logging failure never crashes the
    calculator.

    Args:
        file_path: Path to the log file.  Defaults to ``"error_log.txt"``
            in the current working directory.
    """

    def __init__(self, file_path: str | None = None) -> None:
        if file_path is None:
            self._file_path: pathlib.Path = pathlib.Path("error_log.txt")
        else:
            self._file_path = pathlib.Path(file_path)

    def log_error(
        self,
        error_category: str,
        operation: str,
        inputs: list,
        error_description: str,
    ) -> None:
        """Append one error entry to the log file.

        Args:
            error_category: Category string, e.g. ``"invalid_input"``,
                ``"unsupported_operation"``, or ``"calculation_error"``.
            operation: The operation that caused the error (e.g. ``"add"``).
            inputs: The operands that were provided.  An empty list is
                formatted as an empty string in the entry.
            error_description: Human-readable description of the error.
        """
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        inputs_str = ", ".join(str(x) for x in inputs)
        entry = (
            f"{timestamp} | {error_category} | {operation} | "
            f"{inputs_str} | {error_description}\n"
        )
        try:
            with open(self._file_path, "a", encoding="utf-8") as fh:
                fh.write(entry)
        except Exception:  # noqa: BLE001 — silently swallow all I/O failures
            pass
