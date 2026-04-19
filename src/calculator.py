"""Backward compatibility shim for the Calculator class.

The canonical implementation has moved to :mod:`src.core.calculator`.
This module re-exports ``Calculator`` so that existing import paths
(``from src.calculator import Calculator``) continue to work unchanged.
"""

from src.core.calculator import Calculator

__all__ = ["Calculator"]
