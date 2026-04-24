"""Backward-compatibility facade for the Calculator class.

All implementation has moved to :mod:`~src.calculator_core`.  This module
re-exports :class:`Calculator` so that existing callers using
``from src.calculator import Calculator`` continue to work without changes.

``math`` is imported here so that any callers that rely on
``src.calculator.math`` (e.g. introspection-based checks) continue to find it.
"""

import math  # kept for callers that inspect this module's imports

from .calculator_core import Calculator

__all__ = ["Calculator"]
