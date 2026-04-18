"""Centralized logging configuration for the calculator application.

This module provides a factory function for obtaining configured loggers.
All loggers are created with a NullHandler by default, following library
best practices. Callers can attach their own handlers to enable logging output.

Example:
    import logging
    from src.logger import get_logger

    logger = get_logger(__name__)
    # No output by default. To enable:
    logging.basicConfig(level=logging.ERROR)
    logger.error("An error occurred")
"""

import logging


def get_logger(name: str) -> logging.Logger:
    """Get a configured logger for the given name.

    Returns a logger with a NullHandler attached. Callers are responsible
    for configuring handlers to direct log output to stdout, stderr, or files.

    Args:
        name: The logger name, typically __name__ of the calling module.

    Returns:
        A Logger instance configured with NullHandler.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.addHandler(logging.NullHandler())
    return logger
