"""Backward-compatibility re-export for the Calculator class.

The implementation now lives in ``src.logic.state``.  This module re-exports
``Calculator`` so that existing code using ``from src.calculator import
Calculator`` continues to work without modification.
"""

from src.logic.state import Calculator

__all__ = ["Calculator"]
