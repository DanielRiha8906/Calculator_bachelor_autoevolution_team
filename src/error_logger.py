"""Error logging module for the calculator.

Provides a unified ``log_error`` function and specialised helpers for
logging calculation errors, input validation errors, retry events, and
batch-mode errors to a persistent log file.

The module writes entries in the format::

    [YYYY-MM-DD HH:MM:SS] [ERROR] Operation: <op> | Operands: <list> | Error type: <type> | Error message: <msg>

Each call opens the target file in append mode so earlier entries are
never lost and no log rotation occurs.
"""

from datetime import datetime


# Module-level logger object (kept as a simple sentinel so that
# ``from src.error_logger import error_logger`` succeeds without raising
# an ImportError even when the module is imported before any setup call).
error_logger: object = object()


def setup_logging() -> None:
    """Configure the default error logging destination.

    This is a no-op placeholder that satisfies callers (e.g. ``__main__``)
    that call ``setup_logging()`` at startup.  The actual file-writing is
    performed lazily inside each ``log_*`` function via :func:`log_error`.
    """
    # No global state is needed: log_error() opens the file on every call.
    pass


def log_error(
    operation: str,
    operands: list,
    error_type: str,
    error_message: str,
    filepath: str = "error.log",
) -> None:
    """Write a single structured error entry to the specified log file.

    Opens *filepath* in append mode on every call so that all prior
    entries are preserved and the file grows monotonically (no rotation).

    The written line has the format::

        [YYYY-MM-DD HH:MM:SS] [ERROR] Operation: <op> | Operands: <list> | Error type: <type> | Error message: <msg>

    Args:
        operation: The name of the operation that failed (e.g. ``"divide"``).
        operands: The operand values passed to the operation.
        error_type: The class name of the exception (e.g. ``"ZeroDivisionError"``).
        error_message: The human-readable error description.
        filepath: Path to the log file.  Defaults to ``"error.log"``.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = (
        f"[{timestamp}] [ERROR] "
        f"Operation: {operation} | "
        f"Operands: {operands} | "
        f"Error type: {error_type} | "
        f"Error message: {error_message}\n"
    )
    with open(filepath, "a") as f:
        f.write(line)


def log_calculation_error(
    operation: str,
    operands: list,
    error_type: str,
    error_message: str,
) -> None:
    """Log a domain-level calculation error to the default log file.

    Args:
        operation: The name of the Calculator method that raised the error.
        operands: The operand values supplied to that method.
        error_type: The exception class name (e.g. ``"ValueError"``).
        error_message: The exception message string.
    """
    log_error(operation, operands, error_type, error_message)


def log_input_error(
    field_name: str,
    input_value: str,
    error_type: str,
    error_message: str,
) -> None:
    """Log an interactive-prompt validation error to the default log file.

    Args:
        field_name: A label for the input field (e.g. ``"first number input"``).
        input_value: The raw string value that failed validation.
        error_type: The exception class name (e.g. ``"ValueError"``).
        error_message: The human-readable error description.
    """
    log_error(field_name, [input_value], error_type, error_message)


def log_retry_attempt(
    field_name: str,
    attempt_num: int,
    max_retries: int,
) -> None:
    """Log a single retry attempt for an input field to the default log file.

    Args:
        field_name: A label for the input field being retried.
        attempt_num: The current attempt number (1-based).
        max_retries: The maximum number of allowed attempts.
    """
    log_error(
        field_name,
        [],
        "RetryAttempt",
        f"Invalid input. Attempt {attempt_num}/{max_retries}",
    )


def log_max_retries_exceeded(
    field_name: str,
    error_message: str,
) -> None:
    """Log a MaxRetriesExceeded event for an input field to the default log file.

    Args:
        field_name: A label for the input field that exhausted retries.
        error_message: The human-readable error description.
    """
    log_error(field_name, [], "MaxRetriesExceeded", error_message)


def log_batch_error(
    operation: str,
    operands: list,
    error_type: str,
    error_message: str,
) -> None:
    """Log a batch-mode execution error to the default log file.

    Args:
        operation: The batch operation key (e.g. ``"add"``).
        operands: The operand values (or raw strings) supplied.
        error_type: The exception class name (e.g. ``"ZeroDivisionError"``).
        error_message: The human-readable error description.
    """
    log_error(operation, operands, error_type, error_message)
