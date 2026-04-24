"""Centralized error logging module for the Calculator application.

All user-facing errors (invalid operations, invalid operands, wrong argument
counts, and runtime calculation errors) are appended to ``error.log`` in the
current working directory.  File I/O failures are caught and printed to
stderr so the application never crashes due to a logging failure.
"""

import datetime
import sys
from typing import Any


class ErrorLogger:
    """Appends structured error entries to a log file.

    Each call to a ``log_*`` method writes one line to the log file in append
    mode.  The entry contains a timestamp, an error-type label, and
    context-specific fields.

    Args:
        log_file: Path to the log file.  Defaults to ``"error.log"`` which
            resolves relative to the current working directory.
    """

    def __init__(self, log_file: str = "error.log") -> None:
        self._log_file = log_file

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _timestamp(self) -> str:
        """Return the current local time as a formatted string.

        Returns:
            Timestamp in ``YYYY-MM-DD HH:MM:SS`` format.
        """
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _write(self, entry: str) -> None:
        """Append *entry* followed by a newline to the log file.

        File I/O errors are caught and printed to ``sys.stderr``; they are
        never re-raised so the calling code always continues normally.

        Args:
            entry: The formatted log line to write (without trailing newline).
        """
        try:
            with open(self._log_file, "a") as fh:
                fh.write(entry + "\n")
        except (IOError, OSError, PermissionError) as exc:
            print(f"Warning: could not write to error log: {exc}", file=sys.stderr)

    # ------------------------------------------------------------------
    # Public logging methods
    # ------------------------------------------------------------------

    def log_invalid_operation(self, operation_name: Any, message: str) -> None:
        """Log an unknown or invalid operation error.

        Args:
            operation_name: The name used by the caller (may be ``None``).
            message: Human-readable error description.
        """
        ts = self._timestamp()
        entry = (
            f"[{ts}] [Invalid Operation] "
            f"operation={operation_name}, message={message}"
        )
        self._write(entry)

    def log_invalid_operand(
        self, operation_name: Any, operand_value: Any, message: str
    ) -> None:
        """Log an operand that could not be parsed as a number.

        Args:
            operation_name: The operation being attempted.
            operand_value: The raw value that failed to parse.
            message: Human-readable error description.
        """
        ts = self._timestamp()
        entry = (
            f"[{ts}] [Invalid Operand] "
            f"operation={operation_name}, operand={operand_value}, message={message}"
        )
        self._write(entry)

    def log_incorrect_argument_count(
        self,
        operation_name: Any,
        required: int,
        actual: int,
        message: str,
    ) -> None:
        """Log a mismatch between the expected and actual operand counts.

        Args:
            operation_name: The operation being attempted (may be ``None``).
            required: The number of operands the operation requires.
            actual: The number of operands actually supplied.
            message: Human-readable error description.
        """
        ts = self._timestamp()
        entry = (
            f"[{ts}] [Incorrect Argument Count] "
            f"operation={operation_name}, required={required}, "
            f"actual={actual}, message={message}"
        )
        self._write(entry)

    def log_runtime_calculation_error(
        self,
        operation_name: str,
        operands: Any,
        error_type: str,
        message: str,
    ) -> None:
        """Log an error that occurred during the actual computation.

        Covers domain validation errors (e.g. sqrt of negative), division by
        zero, and any other exception raised by a Calculator method.

        Args:
            operation_name: The operation that was executing when the error
                occurred.
            operands: The operand values passed to the operation (tuple or
                other iterable).
            error_type: The exception class name (e.g. ``"ZeroDivisionError"``).
            message: Human-readable error description.
        """
        ts = self._timestamp()
        entry = (
            f"[{ts}] [Runtime Calculation Error] "
            f"operation={operation_name}, operands={operands}, message={message}"
        )
        self._write(entry)
