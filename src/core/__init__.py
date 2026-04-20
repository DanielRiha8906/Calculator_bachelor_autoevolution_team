"""Core calculation API for the Calculator application.

This package exposes the pure calculation layer — the ``Calculator`` class
and the operation registry builder — with no dependency on interactive UI
or CLI concerns.  Import from here when you only need computation.
"""

from .calculator import Calculator
from .operations import get_operation_registry

__all__ = ["Calculator", "get_operation_registry"]
