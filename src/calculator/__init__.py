"""Calculator package — backward-compatible re-export (Issue #405).

Re-exports Calculator from ``src.calculator.core`` so that existing code
using ``from src.calculator import Calculator`` continues to work unchanged.
"""

from .core import Calculator

__all__ = ["Calculator"]
