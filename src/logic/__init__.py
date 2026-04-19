"""Public interface for the calculator logic layer.

Presentation layers should import ``Calculator`` from here:

    from src.logic import Calculator

Internal modules may import ``ArithmeticEngine`` directly from
``src.logic.core`` if needed.
"""

from src.logic.state import Calculator

__all__ = ["Calculator"]
