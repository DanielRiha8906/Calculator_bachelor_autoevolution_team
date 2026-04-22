# Compatibility shim — re-exports Calculator from its new location.
# Existing consumers (tests, external code) importing `src.calculator.Calculator`
# continue to work without modification.
from .core.calculator import Calculator

__all__ = ["Calculator"]
