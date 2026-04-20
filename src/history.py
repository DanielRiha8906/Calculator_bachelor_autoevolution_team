"""Backward compatibility shim for the HistoryTracker class.

The canonical implementation has moved to :mod:`src.support.history`.
This module re-exports ``HistoryTracker`` so that existing import paths
(``from src.history import HistoryTracker``) continue to work unchanged.
"""

from src.support.history import HistoryTracker

__all__ = ["HistoryTracker"]
