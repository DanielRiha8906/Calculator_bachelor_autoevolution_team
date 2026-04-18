# Backwards-compatibility shim. Import from src.shared instead.
from .shared.dispatcher import OperationDispatcher

__all__ = ["OperationDispatcher"]
