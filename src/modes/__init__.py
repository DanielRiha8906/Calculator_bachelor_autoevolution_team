"""modes — calculator operation mode package.

Exports the public API for operation modes:

- :class:`BasicOperations` — the four arithmetic operations.
- :class:`AdvancedOperations` — advanced mathematical functions.
- :class:`OperationRegistry` — maps operation names to their implementations.
"""

from .basic import BasicOperations
from .advanced import AdvancedOperations
from .operations import OperationRegistry

__all__ = ["BasicOperations", "AdvancedOperations", "OperationRegistry"]
