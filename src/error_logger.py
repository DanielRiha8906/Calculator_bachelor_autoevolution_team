"""Interaction layer service — error logging.

Records and persists error events for auditing and debugging. Part of the
interaction layer; has no direct role in arithmetic computation.

Provides a dedicated :class:`ErrorLogger` for recording categorised error
events to both an in-memory list and a persistent log file.  Errors are
written in a structured, human-readable format so that sessions can be
audited after the fact.

Error categories are exposed as module-level string constants so callers
can reference them without importing an enum:

    * :data:`INVALID_INPUT`
    * :data:`UNSUPPORTED_OPERATION`
    * :data:`CALCULATION_ERROR`
    * :data:`UNEXPECTED_ERROR`
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Error category constants
# ---------------------------------------------------------------------------

INVALID_INPUT: str = "INVALID_INPUT"
UNSUPPORTED_OPERATION: str = "UNSUPPORTED_OPERATION"
CALCULATION_ERROR: str = "CALCULATION_ERROR"
UNEXPECTED_ERROR: str = "UNEXPECTED_ERROR"

#: All recognised category strings — used for validation in tests.
ERROR_CATEGORIES: frozenset[str] = frozenset({
    INVALID_INPUT,
    UNSUPPORTED_OPERATION,
    CALCULATION_ERROR,
    UNEXPECTED_ERROR,
})

# Default log file path (relative to CWD).
_DEFAULT_LOG_FILE: str = "error.log"


class ErrorLogger:
    """Records categorised error events to memory and a log file.

    The log file is opened in *append* mode so that errors from multiple
    sessions accumulate rather than being overwritten.  If the file does
    not exist it is created on the first write.

    Attributes:
        _file_path: Path to the log file (relative to CWD or absolute).
        _history: Ordered list of formatted log entry strings written so
            far in the current session.
    """

    def __init__(self, file_path: str = _DEFAULT_LOG_FILE) -> None:
        """Initialise the logger and ensure the log file exists.

        The file is opened in append mode so previous sessions are
        preserved.  If the file cannot be created an error is written to
        *stderr* and the logger continues operating in memory-only mode.

        Args:
            file_path: Path to the log file.  Defaults to ``"error.log"``
                in the current working directory.
        """
        self._file_path: str = file_path
        self._history: list[str] = []

        # Touch the file so it exists even if no errors are logged yet.
        try:
            with open(self._file_path, "a", encoding="utf-8"):
                pass
        except OSError as exc:
            print(
                f"ErrorLogger: could not initialise log file '{self._file_path}': {exc}",
                file=sys.stderr,
            )

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def log_error(
        self,
        category: str,
        error_message: str,
        context: dict,  # type: ignore[type-arg]
    ) -> None:
        """Append a formatted error entry to memory and the log file.

        File I/O failures are caught and reported to *stderr*; they never
        propagate to the caller so the main program loop is unaffected.

        Args:
            category: One of the module-level category constants
                (e.g. :data:`CALCULATION_ERROR`).
            error_message: Human-readable description of the error.
            context: Arbitrary key-value pairs that provide additional
                debugging context (e.g. operation name, operands).
        """
        timestamp = datetime.now(tz=timezone.utc).isoformat(timespec="seconds")
        entry = self._format_entry(timestamp, category, error_message, context)
        self._history.append(entry)
        try:
            with open(self._file_path, "a", encoding="utf-8") as fh:
                fh.write(entry + "\n")
        except OSError as exc:
            print(
                f"ErrorLogger: failed to write to '{self._file_path}': {exc}",
                file=sys.stderr,
            )

    def get_errors(self) -> list[str]:
        """Return a copy of all error entries recorded this session.

        Returns:
            A list of formatted log entry strings in chronological order.
            Returns an empty list when no errors have been logged yet.
        """
        return list(self._history)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _format_entry(
        self,
        timestamp: str,
        category: str,
        message: str,
        context: dict,  # type: ignore[type-arg]
    ) -> str:
        """Format a single log entry as a structured string.

        The output format is::

            [TIMESTAMP] [CATEGORY] Message | key=value; key=value

        If *context* is empty the trailing ``" | "`` separator is omitted.

        Args:
            timestamp: ISO-8601 timestamp string.
            category: Error category label.
            message: Human-readable error message.
            context: Key-value pairs to append as context fields.

        Returns:
            A single-line formatted log entry string.
        """
        header = f"[{timestamp}] [{category}] {message}"
        if not context:
            return header
        context_str = "; ".join(f"{k}={v}" for k, v in context.items())
        return f"{header} | {context_str}"
