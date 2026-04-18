# Backwards-compatibility shim. Import from src.interface instead.
from .interface.cli import CliDispatcher

__all__ = ["CliDispatcher"]
