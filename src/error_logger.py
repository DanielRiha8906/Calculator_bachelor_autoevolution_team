"""Centralized error logging module for the Calculator application.

Writes structured error records to a log file in append mode, categorised
by error type.  No output is ever written to the console — the logger is
entirely silent to the end-user.
"""

import logging


class ErrorLogger:
    """Typed error logger that appends categorised entries to a log file.

    Each public method corresponds to a distinct calculator error category
    and writes a single ``ERROR``-level log record that includes the
    category label and all relevant input context.

    The underlying :class:`logging.Logger` has **no console handlers**,
    so logging calls produce no visible output to the user.

    Args:
        log_file: Path to the log file.  The file is created on the first
            write and subsequent runs append to it rather than overwriting.

    Example:
        >>> logger = ErrorLogger("error.log")
        >>> logger.log_division_by_zero(10.0)
    """

    def __init__(self, log_file: str = "error.log") -> None:
        self._logger: logging.Logger = logging.getLogger(
            f"{__name__}.{id(self)}"
        )
        self._logger.setLevel(logging.ERROR)
        # Avoid adding duplicate handlers when the module is imported more
        # than once inside the same process (e.g. in tests).
        if not self._logger.handlers:
            handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s"
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
        # Prevent the root logger from also emitting these records to
        # the console.
        self._logger.propagate = False

    def log_unsupported_operation(self, operation_name: str) -> None:
        """Log an attempt to invoke an unknown or unsupported operation.

        Args:
            operation_name: The name of the operation that was requested
                but could not be found.
        """
        self._logger.error(
            "UNSUPPORTED_OPERATION | operation='%s'",
            operation_name,
        )

    def log_invalid_operand(self, operand: str, reason: str) -> None:
        """Log a non-numeric operand that failed parsing.

        Args:
            operand: The raw string value that could not be converted to
                a number.
            reason: A short description of why the conversion failed.
        """
        self._logger.error(
            "INVALID_OPERAND | operand='%s' reason='%s'",
            operand,
            reason,
        )

    def log_incorrect_arity(
        self, operation_name: str, expected: int, got: int
    ) -> None:
        """Log a mismatch between the expected and supplied argument count.

        Args:
            operation_name: The name of the operation whose arity was
                violated.
            expected: The number of operands the operation requires.
            got: The number of operands that were actually supplied.
        """
        self._logger.error(
            "INCORRECT_ARITY | operation='%s' expected=%d got=%d",
            operation_name,
            expected,
            got,
        )

    def log_division_by_zero(self, numerator: float) -> None:
        """Log a division-by-zero attempt.

        Args:
            numerator: The dividend value at the time of the error.
        """
        self._logger.error(
            "DIVISION_BY_ZERO | numerator=%s",
            numerator,
        )

    def log_invalid_domain(
        self, operation_name: str, operand: float, reason: str
    ) -> None:
        """Log a domain error such as sqrt of a negative or log of zero.

        Args:
            operation_name: The name of the operation that raised the
                domain error.
            operand: The out-of-domain value that was supplied.
            reason: A short description of the domain constraint that was
                violated.
        """
        self._logger.error(
            "INVALID_DOMAIN | operation='%s' operand=%s reason='%s'",
            operation_name,
            operand,
            reason,
        )
