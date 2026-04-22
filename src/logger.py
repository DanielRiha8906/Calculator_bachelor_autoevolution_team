"""logger.py — centralized logging configuration for the calculator system.

Provides a factory function that returns pre-configured logger instances
with both console and file handlers.  All modules in this package obtain
their loggers through :func:`get_logger` so that handler and formatter
configuration lives in one place.
"""

from __future__ import annotations

import logging
import logging.handlers

# File to which all DEBUG-and-above records are written.
_LOG_FILE = "calculator.log"

# Module-level flag to ensure the root configuration is applied only once
# even if get_logger() is called multiple times.
_configured: bool = False


def _configure_root_logger() -> None:
    """Set up handlers and formatters on the root logger.

    Called once the first time :func:`get_logger` is invoked.  Subsequent
    calls are no-ops because of the ``_configured`` guard.
    """
    global _configured
    if _configured:
        return

    root = logging.getLogger()
    # Ensure the root logger passes everything down to the handlers; each
    # handler then applies its own level filter.
    root.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler — only WARNING and above to keep stdout clean.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    # File handler — DEBUG and above for full diagnostic output.
    file_handler = logging.FileHandler(_LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    root.addHandler(console_handler)
    root.addHandler(file_handler)

    _configured = True


def get_logger(name: str) -> logging.Logger:
    """Return a pre-configured logger for *name*.

    Initialises the root logger's handlers on the first call so that all
    subsequent loggers automatically inherit the shared console and file
    output configuration.

    Args:
        name: The logger name, typically ``__name__`` of the calling module.

    Returns:
        A :class:`logging.Logger` instance ready to use.

    Example::

        logger = get_logger(__name__)
        logger.error("Something went wrong: %s", exc)
    """
    _configure_root_logger()
    return logging.getLogger(name)
