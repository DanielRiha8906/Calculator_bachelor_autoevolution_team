"""Support package for the Calculator application.

Exports OperationHistory, ErrorLogger, and MaxRetriesExceeded from their
respective submodules.
"""

from .error_logger import ErrorLogger
from .exceptions import MaxRetriesExceeded
from .history import OperationHistory

__all__ = ["ErrorLogger", "MaxRetriesExceeded", "OperationHistory"]
