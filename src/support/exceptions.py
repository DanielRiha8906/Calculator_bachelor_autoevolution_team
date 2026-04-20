"""Custom exceptions for the Calculator application.

Defines application-specific exception types used across the REPL and CLI
interfaces to signal unrecoverable input failure conditions.
"""


class MaxRetriesExceeded(Exception):
    """Raised when maximum input retry attempts have been exceeded."""
