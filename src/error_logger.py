"""Central error logging module for the Calculator application.

Provides consistent, structured error recording across both the CLI and
interactive execution modes.  All errors are appended to ``error.log`` in
the current working directory using Python's standard :mod:`logging`
module — no external dependencies are required.

Log entries use the format::

    TIMESTAMP | ERROR_TYPE | OPERATION | OPERANDS | MESSAGE

where *TIMESTAMP* is an ISO 8601 date-time string.

The canonical class definition lives here; :mod:`src.support.error_logging`
re-exports it for consumers that prefer the new package layout.
"""

import logging
from typing import Any


# ---------------------------------------------------------------------------
# Module-level logger initialisation (singleton pattern)
# ---------------------------------------------------------------------------
_logger = logging.getLogger("calculator.errors")
_logger.setLevel(logging.ERROR)

# Lazy handler: attached only once, on the first call to log_error(), so that
# ``error.log`` is not created for processes that never encounter an error.
_handler_attached: bool = False


def _ensure_handler() -> None:
    """Attach the file handler to the module logger if not yet attached.

    Called lazily on first use so the log file is only created when an
    actual error is recorded.  Any :exc:`OSError` raised while opening the
    file is silently swallowed so that a logging failure never crashes the
    application.
    """
    global _handler_attached  # noqa: PLW0603
    if _handler_attached:
        return
    try:
        handler = logging.FileHandler("error.log", mode="a", encoding="utf-8")
        # Suppress the default date prefix; we embed our own ISO 8601 timestamp
        # inside the message body so the format is fully controlled.
        handler.setFormatter(logging.Formatter("%(message)s"))
        _logger.addHandler(handler)
        # Prevent propagation to the root logger (avoids duplicate console output)
        _logger.propagate = False
        _handler_attached = True
    except OSError:
        pass


class ErrorLogger:
    """Records structured calculator errors to ``error.log``.

    Each instance is lightweight and stateless; all state lives in the
    module-level :data:`_logger`.  Multiple instances may be created freely
    — they all write to the same log file via the shared logger.

    Example::

        error_logger = ErrorLogger()
        error_logger.log_error(
            "INVALID_OPERAND",
            {"operation": "add", "operands": "abc", "message": "not a number"},
        )
    """

    def log_error(self, error_type: str, context: dict[str, Any]) -> None:
        """Record a structured error entry to ``error.log``.

        The entry is written on a single line in the format::

            TIMESTAMP | ERROR_TYPE | OPERATION | OPERANDS | MESSAGE

        where each field is taken from *context* when present (``"operation"``,
        ``"operands"``, ``"message"``).  Missing context fields are rendered as
        ``"N/A"``.  Any :exc:`Exception` raised during formatting or writing is
        silently caught so that logging failures never crash the application.

        Args:
            error_type: A short, uppercase identifier for the error category
                (e.g. ``"INVALID_OPERAND"``, ``"UNSUPPORTED_OPERATION"``).
            context: A dict that may contain any of the following keys:

                * ``"operation"`` – the calculator operation name (str).
                * ``"operands"`` – operand value(s) as a string or any type
                  whose ``str()`` representation is meaningful.
                * ``"message"`` – a human-readable description of the error.

        Returns:
            None
        """
        try:
            _ensure_handler()
            import datetime  # local import keeps module-level namespace clean

            timestamp = datetime.datetime.now().isoformat(timespec="seconds")
            operation = str(context.get("operation", "N/A"))
            operands = str(context.get("operands", "N/A"))
            message = str(context.get("message", "N/A"))

            entry = (
                f"{timestamp} | {error_type} | {operation} | {operands} | {message}"
            )
            _logger.error(entry)
        except Exception:  # noqa: BLE001 — logging must never crash the app
            pass
