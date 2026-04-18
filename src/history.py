# Backwards-compatibility shim. Import from src.session instead.
from .session.history import History

__all__ = ["History"]
