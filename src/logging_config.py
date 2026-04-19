"""Centralized logging configuration for the calculator application.

Log file location: ``calculator.log`` in the working directory (configurable).
Log format: ``<timestamp> <level> <message>``
Default verbosity: ERROR — only error-level events are recorded by default.

Usage::

    from src.logging_config import setup_logging, logger

    # Initialise once at application startup:
    setup_logging()

    # Import the module-level logger directly for convenience:
    logger.error("Something went wrong")
"""

import logging

_LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"


def setup_logging(log_file: str = "calculator.log") -> logging.Logger:
    """Configure and return the application logger.

    Creates a file handler attached to the ``"calculator"`` logger.  The
    handler writes to *log_file* using a timestamp/level/message format and
    records only ERROR-level messages and above by default.

    Calling this function more than once is safe: if handlers are already
    attached to the logger, no duplicate handler is added.

    Args:
        log_file: Path to the log file.  Relative paths are resolved against
            the current working directory at call time.  Defaults to
            ``"calculator.log"``.

    Returns:
        The configured ``logging.Logger`` instance named ``"calculator"``.
    """
    _logger = logging.getLogger("calculator")

    # Avoid adding duplicate handlers on repeated calls.
    if _logger.handlers:
        return _logger

    _logger.setLevel(logging.ERROR)

    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.ERROR)
    handler.setFormatter(logging.Formatter(_LOG_FORMAT))

    _logger.addHandler(handler)
    return _logger


# Module-level logger instance for direct import convenience.
logger: logging.Logger = logging.getLogger("calculator")
