"""Centralised error logging module for the calculator application.

This module provides a dedicated logger that writes structured error records to
``logs/error.log`` relative to the project root.  It exposes three public
helpers covering the three categories of runtime error the calculator produces:

- Validation errors (bad user input / operand parsing)
- Operation errors (unrecognised operation key)
- Calculation errors (domain / arithmetic failures such as division by zero)

The logger is isolated on the ``calculator.errors`` namespace so it never
interferes with the root logger or any other library's logging configuration.

If the log directory or file cannot be created (e.g. due to permission
restrictions), the module falls back silently so that a logging failure never
crashes the calculator itself.
"""

import logging
import os
from typing import List

# ---------------------------------------------------------------------------
# Logger setup
# ---------------------------------------------------------------------------

_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"  # ISO-8601 local time

# Resolve the project root as two levels above this file:
#   src/error_logger.py  ->  src/  ->  <project_root>/
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LOG_DIR = os.path.join(_PROJECT_ROOT, "logs")
_LOG_FILE = os.path.join(_LOG_DIR, "error.log")

_logger = logging.getLogger("calculator.errors")
_logger.setLevel(logging.ERROR)

# Prevent duplicate handlers if the module is imported multiple times (e.g.
# during testing with importlib reloads).
if not _logger.handlers:
    try:
        os.makedirs(_LOG_DIR, exist_ok=True)
        _file_handler = logging.FileHandler(_LOG_FILE, mode="a", encoding="utf-8")
        _file_handler.setLevel(logging.ERROR)
        _file_handler.setFormatter(
            logging.Formatter(fmt=_LOG_FORMAT, datefmt=_DATE_FORMAT)
        )
        _logger.addHandler(_file_handler)
    except OSError:
        # If the log directory or file cannot be created, attach a NullHandler
        # so that log calls are silently discarded rather than raising.
        _logger.addHandler(logging.NullHandler())


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def log_validation_error(detail: str) -> None:
    """Log an invalid-input / operand-parsing error at ERROR level.

    Args:
        detail: A human-readable description of the validation failure,
            typically the string representation of the caught exception.
    """
    try:
        _logger.error("VALIDATION_ERROR: %s", detail)
    except Exception:  # noqa: BLE001 — logging must never crash the app
        pass


def log_operation_error(operation_key: str, error_msg: str) -> None:
    """Log an unsupported-operation error at ERROR level.

    Args:
        operation_key: The operation key string that was not found in the
            registry.
        error_msg: A description of the error, typically ``str(exception)``.
    """
    try:
        _logger.error("OPERATION_ERROR: key=%r — %s", operation_key, error_msg)
    except Exception:  # noqa: BLE001
        pass


def log_calculation_error(operation: str, operands: List, error_msg: str) -> None:
    """Log a calculation-time error (e.g. division by zero, domain error) at ERROR level.

    Args:
        operation: The name of the operation that failed (e.g. ``"divide"``).
        operands: The list of operand values that were passed to the operation.
        error_msg: A description of the error, typically ``str(exception)``.
    """
    try:
        _logger.error(
            "CALCULATION_ERROR: operation=%r operands=%r — %s",
            operation,
            operands,
            error_msg,
        )
    except Exception:  # noqa: BLE001
        pass
