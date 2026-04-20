"""Central error logging module for the Calculator application.

This is the canonical location for the ``ErrorLogger`` class.  The
module-level logging infrastructure (_logger, _handler_attached,
_ensure_handler) lives in :mod:`src.error_logger` and is re-exported here
for completeness.  Import from :mod:`src.error_logger` when you need direct
access to the module-level state.
"""

from src.error_logger import ErrorLogger, _logger, _ensure_handler

__all__ = ["ErrorLogger"]
