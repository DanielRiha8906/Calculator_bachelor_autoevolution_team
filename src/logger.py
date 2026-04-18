"""Centralized error logger for the Calculator application.

This module provides the ``Logger`` class, which wraps Python's standard
``logging`` module with calculator-specific log methods.  All messages are
written in append mode to a plain-text file (default: ``error.log``) so that
successive runs accumulate a persistent audit trail without overwriting previous
entries.

Design notes:
- This module is intentionally separate from ``history.py``.  History records
  *successful* operations for the user's benefit; this logger records *error
  events* for diagnostics and research reproducibility.
- No stack traces are emitted by default; the log format is plain text to keep
  the file human-readable without a log-analysis tool.
- All error-condition methods map to either WARNING or ERROR level, following
  standard severity semantics: WARNING for unexpected-but-recoverable inputs,
  ERROR for conditions that abort the current operation.
"""

from __future__ import annotations

import logging


class Logger:
    """Manages file-based error logging for the calculator.

    Opens (or creates) *log_file* in append mode on construction.
    Subsequent calls to the log methods write plain-text lines at the
    appropriate severity level.  The file is never truncated between runs.

    Args:
        log_file: Path to the log file.  Defaults to ``"error.log"``.
    """

    def __init__(self, log_file: str = "error.log") -> None:
        self._logger = logging.getLogger(f"calculator.{log_file}")
        # Avoid adding duplicate handlers when the same logger name is reused
        # (e.g. in tests that instantiate Logger multiple times).
        if not self._logger.handlers:
            handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
            handler.setFormatter(
                logging.Formatter(
                    fmt="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            )
            self._logger.addHandler(handler)
        self._logger.setLevel(logging.WARNING)

    # ------------------------------------------------------------------
    # Public log methods
    # ------------------------------------------------------------------

    def log_unsupported_operation(self, operation: str) -> None:
        """Log an unknown/unsupported operation request at WARNING level.

        Args:
            operation: The operation string entered by the user or passed via
                CLI that is not present in the OPERATIONS registry.
        """
        self._logger.warning("Unsupported operation requested: '%s'", operation)

    def log_invalid_operand(self, raw_value: str, expected_type: str) -> None:
        """Log a coercion failure for a raw operand value at ERROR level.

        Args:
            raw_value: The raw string that could not be converted.
            expected_type: Human-readable description of the expected type
                (e.g. ``"<numeric>"``).
        """
        self._logger.error(
            "Invalid operand '%s': could not coerce to %s",
            raw_value,
            expected_type,
        )

    def log_invalid_argument_count(
        self, operation: str, expected: int, given: int
    ) -> None:
        """Log an arity mismatch at ERROR level.

        Args:
            operation: The operation key that was invoked.
            expected: The number of operands the operation requires.
            given: The number of operands actually supplied.
        """
        self._logger.error(
            "Argument count mismatch for '%s': expected %d, got %d",
            operation,
            expected,
            given,
        )

    def log_division_by_zero(self, operands: list) -> None:
        """Log a division-by-zero attempt at ERROR level.

        Args:
            operands: The operand list that triggered the error, logged for
                context.
        """
        self._logger.error(
            "Division by zero attempted with operands: %s", operands
        )

    def log_domain_error(self, operation: str, error_message: str) -> None:
        """Log a domain constraint violation at ERROR level.

        Covers both ``ValueError`` (e.g. square root of a negative number) and
        ``TypeError`` (e.g. non-numeric argument passed to a math function).

        Args:
            operation: The operation key that triggered the error.
            error_message: The string representation of the caught exception.
        """
        self._logger.error(
            "Domain error in operation '%s': %s", operation, error_message
        )
