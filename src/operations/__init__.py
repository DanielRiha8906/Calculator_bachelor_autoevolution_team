"""Operation registry composition layer for the Calculator application.

Merges NORMAL_OPERATIONS and SCIENTIFIC_OPERATIONS into a unified OPERATIONS
dict exported from this package.
"""

from .normal import NORMAL_OPERATIONS
from .scientific import SCIENTIFIC_OPERATIONS

OPERATIONS: dict[str, dict] = {**NORMAL_OPERATIONS, **SCIENTIFIC_OPERATIONS}

__all__ = ["OPERATIONS", "NORMAL_OPERATIONS", "SCIENTIFIC_OPERATIONS"]
